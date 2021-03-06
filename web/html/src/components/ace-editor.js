/* eslint-disable */
'use strict';

import PropTypes from 'prop-types';
import * as React from 'react';
import ReactDOM from 'react-dom';

class AceEditor extends React.Component {
  static propTypes = {
    mode: PropTypes.string,
    content: PropTypes.string,
    className: PropTypes.string,
    id: PropTypes.string,
    minLines: PropTypes.number,
    maxLines: PropTypes.number,
    readOnly: PropTypes.bool,
    name: PropTypes.string,
    onChange: PropTypes.func,
  };

  componentDidMount() {
    const component = this;

    const node = ReactDOM.findDOMNode(component.refs.editor);
    const editor = ace.edit(node);
    editor.setTheme("ace/theme/xcode");
    editor.getSession().setMode("ace/mode/" + component.props.mode);
    editor.setShowPrintMargin(false);
    editor.setOptions({minLines: component.props.minLines});
    editor.setOptions({maxLines: component.props.maxLines});
    editor.setReadOnly(component.props.readOnly);

    editor.getSession().on('change', function() {
      component.props.onChange(editor.getSession().getValue());
    });
  }

  render() {
    return (
      <div ref="editor" className={this.props.className} id={this.props.id}>
        {this.props.content}
      </div>
    );
  }
}

export {
    AceEditor,
};
