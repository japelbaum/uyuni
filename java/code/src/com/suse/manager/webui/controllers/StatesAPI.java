/**
 * Copyright (c) 2015 SUSE LLC
 *
 * This software is licensed to you under the GNU General Public License,
 * version 2 (GPLv2). There is NO WARRANTY for this software, express or
 * implied, including the implied warranties of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
 * along with this software; if not, see
 * http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
 *
 * Red Hat trademarks are not licensed under GPLv2. No permission is
 * granted to use or replicate Red Hat trademarks that are incorporated
 * in this software or its documentation.
 */
package com.suse.manager.webui.controllers;

import com.redhat.rhn.domain.rhnpackage.PackageArch;
import com.redhat.rhn.domain.rhnpackage.PackageEvr;
import com.redhat.rhn.domain.server.Server;
import com.redhat.rhn.domain.server.ServerFactory;
import com.redhat.rhn.domain.state.PackageState;
import com.redhat.rhn.domain.state.ServerStateRevision;
import com.redhat.rhn.domain.state.StateFactory;
import com.redhat.rhn.domain.user.User;
import com.redhat.rhn.manager.rhnpackage.PackageManager;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import com.suse.manager.webui.services.SaltService;
import com.suse.manager.webui.services.impl.SaltAPIService;
import com.suse.manager.webui.utils.gson.JSONPackageState;
import com.suse.manager.webui.utils.gson.JSONServerApplyStates;
import com.suse.manager.webui.utils.gson.JSONServerPackageStates;
import com.suse.manager.webui.utils.salt.Grains;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

import spark.Request;
import spark.Response;

/**
 * Controller class providing the backend for API calls to work with states.
 */
public class StatesAPI {

    private static final Gson GSON = new GsonBuilder().create();
    private static final SaltService SALT_SERVICE = SaltAPIService.INSTANCE;

    private StatesAPI() { }

    /**
     * Query the current list of package states for a given server.
     *
     * @param request the request object
     * @param response the response object
     * @return JSON result of the API call
     */
    public static String packages(Request request, Response response) {
        String serverId = request.queryParams("sid");
        Server server = ServerFactory.lookupById(Long.valueOf(serverId));

        response.type("application/json");
        return GSON.toJson(currentPackageStates(server));
    }

    /**
     * Find matches among this server's current packages states as well as among the
     * available packages and convert to JSON.
     *
     * @param request the request object
     * @param response the response object
     * @return JSON result of the API call
     */
    public static String match(Request request, Response response) {
        String target = ".*" + request.queryParams("target") + ".*";
        String serverId = request.queryParams("sid");

        // Find matches among this server's current packages states
        Server server = ServerFactory.lookupById(Long.valueOf(serverId));
        Set<JSONPackageState> matchingCurrent = currentPackageStates(server).stream()
                .filter(p -> p.getName().matches(target))
                .collect(Collectors.toSet());

        // Find matches among available packages and convert to JSON objects
        Set<JSONPackageState> matchingAvailable = PackageManager
                .systemTotalPackages(Long.valueOf(serverId), null).stream()
                .filter(p -> p.getName().matches(target))
                .map(p -> new JSONPackageState(p.getName(), new PackageEvr(
                        p.getEpoch(), p.getVersion(), p.getRelease()), p.getArch()))
                .collect(Collectors.toSet());

        response.type("application/json");
        return GSON.toJson(matchingCurrent.addAll(matchingAvailable));
    }

    /**
     * Save a new state revision for a server based on the latest existing revision and an
     * incoming list of changed package states in the request body.
     *
     * @param request the request object
     * @param response the response object
     * @param user the user
     * @return null to make spark happy
     */
    public static Object save(Request request, Response response, User user) {
        JSONServerPackageStates json = GSON.fromJson(request.body(),
                JSONServerPackageStates.class);
        Server server = ServerFactory.lookupById(json.getServerId());

        // Create a new state revision for this server
        ServerStateRevision state = new ServerStateRevision();
        state.setServer(server);
        state.setCreator(user);

        // Get the latest package states, convert to JSON and merge with the changes
        Set<JSONPackageState> jsonLatestStates = new HashSet<>();
        Optional<Set<PackageState>> latestStates = StateFactory.latestPackageStates(server);
        if (latestStates.isPresent()) {
            jsonLatestStates = convertToJSON(latestStates.get());
        }
        json.getPackageStates().addAll(jsonLatestStates);

        // Add only valid states to the new revision, unmanaged packages will be skipped
        json.getPackageStates().stream().forEach(pkgState ->
                 pkgState.convertToPackageState().ifPresent(state::addPackageState));
        StateFactory.save(state);
        return null;
    }

    /**
     * Apply a list of states to a minion and return the results as JSON.
     *
     * @param request the request object
     * @param response the response object
     * @return JSON results of state application
     */
    public static Object apply(Request request, Response response) {
        JSONServerApplyStates json = GSON.fromJson(request.body(),
                JSONServerApplyStates.class);
        Server server = ServerFactory.lookupById(Long.valueOf(json.getServerId()));
        Map<String, Map<String, Object>> results = SALT_SERVICE.applyState(
                new Grains("machine_id", server.getDigitalServerId()), json.getStates());

        response.type("application/json");
        return GSON.toJson(results);
    }

    /**
     * Get the current set of package states for a given server.
     *
     * @param server the server
     * @return the current set of package states
     */
    private static Set<JSONPackageState> currentPackageStates(Server server) {
        // Lookup all revisions and take package states from the latest one
        List<ServerStateRevision> stateRevisions =
                StateFactory.lookupServerStateRevisions(server);
        Set<PackageState> packageStates = new HashSet<>();
        if (stateRevisions != null && !stateRevisions.isEmpty()) {
            packageStates = stateRevisions.get(0).getPackageStates();
        }

        return convertToJSON(packageStates);
    }

    /**
     * Convert a given set of {@link PackageState} objects into a set of
     * {@link JSONPackageState} objects.
     *
     * @param packageStates the set of package states
     * @return set of JSON objects
     */
    private static Set<JSONPackageState> convertToJSON(Set<PackageState> packageStates) {
        return packageStates.stream().map(state ->
            new JSONPackageState(
                    state.getName().getName(),
                    Optional.ofNullable(state.getEvr())
                            .orElse(new PackageEvr("", "", "")),
                    Optional.ofNullable(state.getArch())
                            .map(PackageArch::getLabel).orElse(""),
                    Optional.of(state.getPackageStateTypeId()),
                    Optional.of(state.getVersionConstraintId())
            )
        ).collect(Collectors.toSet());
    }
}
