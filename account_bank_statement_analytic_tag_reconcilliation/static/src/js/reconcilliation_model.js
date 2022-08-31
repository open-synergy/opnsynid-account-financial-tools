/*
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
*/
odoo.define('account_bank_statement_analytic_tag_reconcilliation.ReconciliationModel', function (require) {
    "use strict";

    var core = require('web.core');
    var ReconciliationModel = require('account.ReconciliationModel');
    var _t = core._t;

    ReconciliationModel.StatementModel.include({
        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.extra_field_names = ['analytic_tag_ids'];
            this.quickCreateFields = this.quickCreateFields.concat(this.extra_field_names);
        },

        quickCreateProposition: function (handle, reconcileModelId) {
            var line = this.getLine(handle);
            var reconcileModel = _.find(this.reconcileModels, function (r) {return r.id === reconcileModelId;});
            var fields = ['account_id', 'amount', 'amount_type', 'analytic_account_id', 'journal_id', 'label', 'tax_id', 'analytic_tag_ids'];
            this._blurProposition(handle);

            var focus = this._formatQuickCreate(line, _.pick(reconcileModel, fields));
            focus.reconcileModelId = reconcileModelId;
            line.reconciliation_proposition.push(focus);

            if (reconcileModel.has_second_line) {
                var second = {};
                _.each(fields, function (key) {
                    second[key] = ("second_"+key) in reconcileModel ? reconcileModel["second_"+key] : reconcileModel[key];
                });
                focus = this._formatQuickCreate(line, second);
                focus.reconcileModelId = reconcileModelId;
                line.reconciliation_proposition.push(focus);
                this._computeReconcileModels(handle, reconcileModelId);
            }
            line.createForm = _.pick(focus, this.quickCreateFields);
            return this._computeLine(line);
        },

        _formatMany2ManyTags: function (value) {
            var res = [];

            for (var i=0, len=value.length; i<len; i++) {
                res[i] = {'id': value[i][0], 'display_name': value[i][1]};
            }

            return res;
        },

        _formatQuickCreate: function (line, values) {
            var result = this._super(line, values);
            values = values || {};

            result['analytic_tag_ids'] = this._formatMany2ManyTags(values.analytic_tag_ids || []);

            return result;
        },

        updateProposition: function (handle, values) {
            var self = this;
            var line = this.getLine(handle);
            var prop = _.last(_.filter(line.reconciliation_proposition, '__focus'));
            if (!prop) {
                prop = this._formatQuickCreate(line);
                line.reconciliation_proposition.push(prop);
            }
            _.each(values, function (value, fieldName) {
                if (fieldName === 'analytic_tag_ids') {
                    switch (value.operation) {
                        case "ADD_M2M":
                            if (!_.findWhere(prop.analytic_tag_ids, {id: value.ids.id})) {
                                prop.analytic_tag_ids.push(value.ids);
                            }
                            break;
                        case "FORGET": 
                            var id = parseInt(self.localData[value.ids[0]].ref);
                            prop.analytic_tag_ids = _.filter(prop.analytic_tag_ids, function (val) {
                                return val.id !== id;
                            });
                            break;
                    }
                } else {
                    prop[fieldName] = values[fieldName];
                }
            });
            if ('account_id' in values) {
                prop.account_code = prop.account_id ? this.accounts[prop.account_id.id] : '';
            }
            if ('amount' in values) {
                prop.base_amount = values.amount;
                if (prop.reconcileModelId) {
                    this._computeReconcileModels(handle, prop.reconcileModelId);
                }
            }
            if ('account_id' in values || 'amount' in values || 'tax_id' in values) {
                prop.__tax_to_recompute = true;
            }
            line.createForm = _.pick(prop, this.quickCreateFields);
            return this._computeLine(line);
        },

        _formatToProcessReconciliation: function (line, prop) {
            var result = this._super(line, prop);

            result['analytic_tag_ids'] = [[6, null, _.pluck(prop.analytic_tag_ids, 'id')]];

            return result;
        },

    });

});