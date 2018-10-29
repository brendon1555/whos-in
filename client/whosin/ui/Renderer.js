/**
 * Copyright 2015, Anomaly Software
 */
goog.provide('whosin.ui.Renderer');

goog.require('goog.dom.classlist');
goog.require('goog.ui.Component');


/**
 * @constructor
 * @suppress {undefinedVars}
 *
 * @extends {goog.ui.Component}
 */
whosin.ui.Renderer = function() {
    whosin.ui.Renderer.base(this, 'constructor');
};
goog.inherits(whosin.ui.Renderer, goog.ui.Component);

/**
 * @override
 */
whosin.ui.Renderer.prototype.canDecorate = function() {
    return true;
};

/**
 * @override
 */
whosin.ui.Renderer.prototype.enterDocument = function() {

    whosin.ui.Renderer.base(this, 'enterDocument');

    var element_ = this.getElement();
};

/**
 * @override
 */
whosin.ui.Renderer.prototype.exitDocument = function() {
    whosin.ui.Renderer.base(this, 'exitDocument');
};

/**
 * Start the application
 */
goog.events.listen(window, goog.events.EventType.LOAD, /** @suppress {undefinedVars} */ function(){
    var appUI_ = new whosin.ui.Renderer();

    goog.dom.removeChildren(document.body);
    appUI_.decorate(document.body);
});