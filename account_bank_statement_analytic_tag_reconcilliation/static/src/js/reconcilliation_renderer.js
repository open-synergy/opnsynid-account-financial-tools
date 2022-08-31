/*
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
*/
odoo.define('account_bank_statement_analytic_tag_reconcilliation.ReconciliationRenderer', function (require) {
    "use strict";

    var core = require('web.core');
    var relational_fields = require('web.relational_fields');
    var basic_fields = require('web.basic_fields');
    var ReconciliationRenderer = require('account.ReconciliationRenderer');
    var qweb = core.qweb;
    var _t = core._t;

    ReconciliationRenderer.LineRenderer.include({
        update: function (state) {
            var self = this;
            // isValid
            this.$('caption .o_buttons button.o_validate').toggleClass('hidden', !!state.balance.type);
            this.$('caption .o_buttons button.o_reconcile').toggleClass('hidden', state.balance.type <= 0);
            this.$('caption .o_buttons .o_no_valid').toggleClass('hidden', state.balance.type >= 0);

            // partner_id
            this._makePartnerRecord(state.st_line.partner_id, state.st_line.partner_name).then(function (recordID) {
                self.fields.partner_id.reset(self.model.get(recordID));
                self.$el.attr('data-partner', state.st_line.partner_id);
            });

            // mode
            this.$('.create, .match').each(function () {
                var $panel = $(this);
                $panel.css('-webkit-transition', 'none');
                $panel.css('-moz-transition', 'none');
                $panel.css('-o-transition', 'none');
                $panel.css('transition', 'none');
                $panel.css('max-height', $panel.height());
                $panel.css('-webkit-transition', '');
                $panel.css('-moz-transition', '');
                $panel.css('-o-transition', '');
                $panel.css('transition', '');
            });
            this.$el.data('mode', state.mode).attr('data-mode', state.mode);
            this.$('.create, .match').each(function () {
                $(this).removeAttr('style');
            });

            // reconciliation_proposition
            var $props = this.$('.accounting_view tbody').empty();

            // loop state propositions
            var props = [];
            var nb_debit_props = 0;
            var nb_credit_props = 0;
            _.each(state.reconciliation_proposition, function (prop) {
                if (prop.display) {
                    props.push(prop);
                    if (prop.amount < 0)
                        nb_debit_props += 1;
                    else if (prop.amount > 0)
                        nb_credit_props += 1;
                }
            });

            _.each(props, function (line) {
                var $line = $(qweb.render("reconciliation.line.mv_line", {'line': line, 'state': state}));
                if (!isNaN(line.id)) {
                    $('<span class="line_info_button fa fa-info-circle"/>')
                        .appendTo($line.find('.cell_info_popover'))
                        .attr("data-content", qweb.render('reconciliation.line.mv_line.details', {'line': line}));
                }
                if (line.already_paid === false &&
                    ((state.balance.amount_currency < 0 || line.partial_reconcile) && nb_credit_props == 1
                        && line.amount > 0 && state.st_line.amount > 0 && state.st_line.amount < line.amount) ||
                    ((state.balance.amount_currency > 0 || line.partial_reconcile) && nb_debit_props == 1
                        && line.amount < 0 && state.st_line.amount < 0 && state.st_line.amount > line.amount)) {
                    var $cell = $line.find(line.amount > 0 ? '.cell_right' : '.cell_left');
                    var text;
                    if (line.partial_reconcile) {
                        text = _t("Undo the partial reconciliation.");
                        $cell.text(line.write_off_amount_str);
                    } else {
                        text = _t("This move's amount is higher than the transaction's amount. Click to register a partial payment and keep the payment balance open.");
                    }

                    $('<span class="do_partial_reconcile_'+(!line.partial_reconcile)+' line_info_button fa fa-exclamation-triangle"/>')
                        .prependTo($cell)
                        .attr("data-content", text);
                }
                $props.append($line);
            });

            // mv_lines
            var $mv_lines = this.$('.match table tbody').empty();
            _.each(state.mv_lines.slice(0, state.limitMoveLines), function (line) {
                var $line = $(qweb.render("reconciliation.line.mv_line", {'line': line, 'state': state}));
                if (!isNaN(line.id)) {
                    $('<span class="line_info_button fa fa-info-circle"/>')
                        .appendTo($line.find('.cell_info_popover'))
                        .attr("data-content", qweb.render('reconciliation.line.mv_line.details', {'line': line}));
                }
                $mv_lines.append($line);
            });
            this.$('.match .fa-chevron-right').toggleClass('disabled', state.mv_lines.length <= state.limitMoveLines);
            this.$('.match .fa-chevron-left').toggleClass('disabled', !state.offset);
            this.$('.match').css('max-height', !state.mv_lines.length && !state.filter.length ? '0px' : '');

            // balance
            this.$('.popover').remove();
            this.$('table tfoot').html(qweb.render("reconciliation.line.balance", {'state': state}));

            // filter
            if (_.str.strip(this.$('input.filter').val()) !== state.filter) {
                this.$('input.filter').val(state.filter);
            }

            // create form
            if (state.createForm) {
                if (!this.fields.account_id) {
                    this._renderCreate(state);
                }
                var data = this.model.get(this.handleCreateRecord).data;
                this.model.notifyChanges(this.handleCreateRecord, state.createForm)
                    .then(function () {
                        return self.model.notifyChanges(self.handleCreateRecord, {analytic_tag_ids: {operation: 'REPLACE_WITH', ids: _.pluck(state.createForm.analytic_tag_ids, 'id')}})
                    })
                    .then(function () {
                        var record = self.model.get(self.handleCreateRecord);
                        _.each(self.fields, function (field, fieldName) {
                            if (self._avoidFieldUpdate[fieldName]) return;
                            if (fieldName === "partner_id") return;
                            if ((data[fieldName] || state.createForm[fieldName]) && !_.isEqual(state.createForm[fieldName], data[fieldName])) {
                                field.reset(record);
                            }
                        });
                    });
            }
            this.$('.create .add_line').toggle(!!state.balance.amount_currency);
        },

        _renderCreate: function (state) {
            var self = this;
            this.model.makeRecord('account.bank.statement.line', [{
                relation: 'account.account',
                type: 'many2one',
                name: 'account_id',
            }, {
                relation: 'account.journal',
                type: 'many2one',
                name: 'journal_id',
            }, {
                relation: 'account.tax',
                type: 'many2one',
                name: 'tax_id',
            }, {
                relation: 'account.analytic.account',
                type: 'many2one',
                name: 'analytic_account_id',
            }, {
                type: 'char',
                name: 'label',
            }, {
                relation: 'account.analytic.tag',
                type: 'many2many',
                name: 'analytic_tag_ids',
                fields: [{
                    name: 'id',
                    type: 'integer',
                }, {
                    name: 'display_name',
                    type: 'char',
                }],
            }, {
                type: 'float',
                name: 'amount',
            }], {
                account_id: {string: _t("Account")},
                label: {string: _t("Label")},
                amount: {string: _t("Account")}
            }).then(function (recordID) {
                self.handleCreateRecord = recordID;
                var record = self.model.get(self.handleCreateRecord);

                self.fields.account_id = new relational_fields.FieldMany2One(self,
                    'account_id', record, {mode: 'edit'});

                self.fields.journal_id = new relational_fields.FieldMany2One(self,
                    'journal_id', record, {mode: 'edit'});

                self.fields.tax_id = new relational_fields.FieldMany2One(self,
                    'tax_id', record, {mode: 'edit'});

                self.fields.analytic_account_id = new relational_fields.FieldMany2One(self,
                    'analytic_account_id', record, {mode: 'edit'});

                self.fields.label = new basic_fields.FieldChar(self,
                    'label', record, {mode: 'edit'});

                self.fields.amount = new basic_fields.FieldFloat(self,
                    'amount', record, {mode: 'edit'});

                self.fields.analytic_tag_ids = new relational_fields.FieldMany2ManyTags(self,
                    'analytic_tag_ids', record, { mode: 'edit' });

                var domain = [['id', '=', state.st_line.journal_id]];
                var fields = ['type'];
                self._rpc({
                    model: 'account.journal',
                    method: 'search_read',
                    args: [domain, fields],
                }).then(function (result) {
                    var journal_type = '';
                    if (result[0]) {
                        journal_type = result[0].type;
                    }
                    var $create = $(qweb.render("reconciliation.line.create", {'state': state, 'journal_type': journal_type}));
                    self.fields.account_id.appendTo($create.find('.create_account_id .o_td_field'))
                        .then(addRequiredStyle.bind(self, self.fields.account_id));
                    self.fields.journal_id.appendTo($create.find('.create_journal_id .o_td_field'));
                    self.fields.tax_id.appendTo($create.find('.create_tax_id .o_td_field'));
                    self.fields.analytic_account_id.appendTo($create.find('.create_analytic_account_id .o_td_field'));
                    self.fields.analytic_tag_ids.appendTo($create.find('.create_analytic_tag_ids .o_td_field'));
                    self.fields.label.appendTo($create.find('.create_label .o_td_field'))
                        .then(addRequiredStyle.bind(self, self.fields.label));
                    self.fields.amount.appendTo($create.find('.create_amount .o_td_field'))
                        .then(addRequiredStyle.bind(self, self.fields.amount));
                    self.$('.create').append($create);

                    function addRequiredStyle(widget) {
                        widget.$el.addClass('o_required_modifier');
                    }
                });
            });
        },
    });

});