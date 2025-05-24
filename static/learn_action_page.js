// HP-937, HP-957, HP-956
(function ($) {
    $(function () {
        $('[data-cms-content]').each(function (index, elem) {

            var $this = $(elem),
                options = JSON.parse($this.attr('data-cms-content')),
                callback = options.callback,
                section = typeof options['section'] !== 'undefined' ? options['section'] : '.content',
                cmspageuri = options.cms_page_uri;

            if (typeof cmspageuri === 'undefined') {
                return true;
            }

            $this.cmspage({
                pageName: options['cms_page_uri'],
                section: section
            }).on('cmspageloadcompleted', function (event, response) {
                console.log('cmspageloadcompleted');
                // after the content is loaded
                // reinitialize the jig-grid and jig-tabs
                var $tabs = $this.find('.jig-ncbitabs');
                if ($tabs.length) {
                    $tabs.ncbitabs();
                }

                var $grids = $this.find('.jig-ncbigrid');
                if ($grids.length) {
                    $grids.ncbigrid({
                        'filterToolbarEnabled': true,
                        'filterToolbarIsCaseInsensitive': true
                    });
                }

                if (typeof callback !== 'undefined' && window[callback] !== 'undefined') {
                    if (typeof options.args !== 'undefined') {
                        window[callback].call(elem, options.args);
                    } else {
                        window[callback].call(elem);
                    }
                }

                $.publish('cmspageloadcompleted', {$el: $this});
            });
        }); // end each

    });
})(jQuery);

// provide a custom sort function to jig grid
function sortCustomDate(firstRow, secRow) {

    var aD = firstRow.row.children().first().text();
    var bD = secRow.row.children().first().text();

    var aD_dt_str = createDateObject(aD);
    var bD_dt_str = createDateObject(bD);

    if (aD_dt_str.isBefore(bD_dt_str)) {
        return this.options.sortColumnDir;
    }
    else if (aD_dt_str.isAfter(bD_dt_str)) {
        return -this.options.sortColumnDir;
    }
    else {
        return 0;
    }
}

function createDateObject(strDate) {
    strDate = strDate.trim();

    //May 01, 2015 & May 15, 2015
    //May 01, 2015 - May 15, 2015
    var p1 = /^([a-z]{3,} \d{1,2}, \d{4}) (&|-) ([a-z]{3,} \d{1,2}, \d{4})$/gi;

    // March 18, 2015
    var p2 = /^([a-z]{3,} \d{1,2}, \d{4})$/gi;

    var arr = [];
    var momentDate;

    if (arr = p1.exec(strDate)) {
        strDate = arr[1];
        momentDate = moment(strDate, ['MMM DD, YYYY', 'MMMM DD, YYYY']);
    }
    else if (arr = p2.exec(strDate)) {
        strDate = arr[1];
        momentDate = moment(strDate, ['MMM DD, YYYY', 'MMMM DD, YYYY']);
    }
    else {
        // assume that is strDate is MMM DD, YYYY OR MMMM, DD YYYY
        momentDate = moment(strDate, ['MMM DD, YYYY', 'MMMM DD, YYYY']);
    }

    return momentDate;
}

function populate_event_table_with_grouping() {
    var DEFAULT_GRID_OPTIONS = {
        collapseRowsEnabled: true
    };

    if (typeof GRID_OPTIONS !== 'undefined') {
        // this enable putting the config object in CMS
        jQuery.extend(DEFAULT_GRID_OPTIONS, GRID_OPTIONS);
    }

    var $grid = jQuery('#exhibit-table');
    $grid.ncbigrid(DEFAULT_GRID_OPTIONS);

    $grid.find('tbody th').css({
        'background': '#369',
        'color': '#fff',
        'font-weight': 'bold',
        'font-size': 'larger'
    });
}

//
// from portal's education site
function populate_event_tables() {

    var expandOptions = {minHeight: '55px'};
    var gridOptions = {
        sortColumn: 1,
        filterToolbarIsCaseInsensitive: true,
        filterToolbarEnabled: true,
        isSortable: true
    };

    if (typeof GRID_OPTIONS !== 'undefined') {
        // this enable putting the config object in CMS
        jQuery.extend(gridOptions, GRID_OPTIONS);
    }

    var $originalTable = jQuery('#original_table');
    var now = moment();

    $originalTable.each(function () {

        var $oTable = jQuery(this);
        var number_of_columns = typeof $oTable.attr('data-num-of-columns') == 'undefined' ? 4 : $oTable.attr('data-num-of-columns');

        var $futureTable = jQuery("#future_table");
        var $pastTable = jQuery("#past_table");

        $futureTable.on("ncbigridcolumnsorted", function (event, ui) {
            $futureTable.find('tbody tr').removeClass("mkhoz").not(':last').addClass("mkhoz");
        });

        $pastTable.on("ncbigridcolumnsorted", function (event, ui) {
            $pastTable.find('tbody tr').removeClass("mkhoz").not(':last').addClass("mkhoz");
        });

        var arr_arg = $futureTable.find("thead tr th");

        if (typeof gridOptions['sortFunctions'] === 'undefined' && gridOptions['isSortable'] === true) {
            var map_var = jQuery.map(arr_arg, function () {
                return null;
            });

            map_var[0] = sortCustomDate;
            gridOptions['sortFunctions'] = map_var;
        }

        $originalTable.find("tbody tr").each(function (index) {
            var web_dat = jQuery(this).children().first().text();
            web_dat = createDateObject(web_dat);

            // if date is not valid, do not show the row
            if (web_dat.isValid()) {
                var trElement = jQuery("<tr></tr>");
                // future or today
                if (web_dat.isAfter(now) || (web_dat.date() == now.date() &&
                    web_dat.month() == now.month() &&
                    web_dat.year() == now.year())) {

                    trElement.append(jQuery(this).children(":not(:eq(5))"));
                    $futureTable.find("tbody").append(trElement);
                }
                else {
                    trElement.append(jQuery(this).children(":not(:eq(" + number_of_columns + "))"));
                    $pastTable.find("tbody").append(trElement);
                }
            }
        });

        $futureTable.ncbigrid(gridOptions);
        // for past table, remove the sort see HP-
        gridOptions['sortColumnDir'] = 1;
        $pastTable.ncbigrid(gridOptions);

        $futureTable.parent().prev().children().first().text("Search:");
        $pastTable.parent().prev().children().first().text("Search:");
        $futureTable.find("tbody tr td").addClass("mk_top");
        $pastTable.find("tbody tr td").addClass("mk_top");
        $futureTable.find('tbody tr').removeClass("mkhoz").not(':last').addClass("mkhoz");
        $pastTable.find('tbody tr').removeClass("mkhoz").not(':last').addClass("mkhoz");

        // if there is no future/past event, just add a row "no archived/upcoming courses & webinars"
        if ($futureTable.find('tbody tr').length == 0) {
            $futureTable.append('<tbody><tr><td colspan="6">No upcoming courses & webinars.</td></tr></tbody>')
        }

        if ($pastTable.find('tbody tr').length == 0) {
            $pastTable.append('<tbody><tr><td colspan="6">No archived courses & webinars.</td></tr></tbody>')
        }

        jQuery.publish('add-a-clear-button-to-jiggrid-filter-textbox', {
            $tables: [$futureTable, $pastTable]
        });
    });
}

function populate_tutorial_table() {
    console.info('populate_tutorial_table');
    var DEFAULT_GRID_OPTIONS = {
        sortColumn: 1,
        filterToolbarIsCaseInsensitive: true,
        filterToolbarEnabled: true,
        isSortable: true,
        columnTypes: ['str-insensitive', 'str-insensitive'],
        sortColumn: 2
    };

    if (typeof GRID_OPTIONS !== 'undefined') {
        // this enable putting the config object in CMS
        jQuery.extend(DEFAULT_GRID_OPTIONS, GRID_OPTIONS);
    }

    var $table = jQuery('#tutorial-table').ncbigrid(DEFAULT_GRID_OPTIONS);

    jQuery.publish('add-a-clear-button-to-jiggrid-filter-textbox', {$tables: [$table]});
}

function populate_documentation_table() {
    var $table = jQuery('#documentations').find('.jig-ncbigrid');
    jQuery.publish('add-a-clear-button-to-jiggrid-filter-textbox', {$tables: [$table]});
    //If there is a param filter in the url, put in the jig-grid filter textbox
    var filter = getParamValue("filter");
    if (filter !== "") {
        var $gridFilterTextBox = jQuery('#documentations .ui-ncbigrid-filter-toolbar input[name="gridFilter"]');
        $gridFilterTextBox.val(filter)
            .trigger('keyup');
    }
}

(function ($) {
    $(function () {

        var $maincontent = $('#maincontent');
        // rather than attaching the event listener to #maincontent
        // we could override jQuery.ui.ncbijiggrid.prototype._filterGrid but that would mean more work
        $maincontent.on('ncbigridfilterapplied', 'table', function (a, b) {
            var $gridWithFilterToolbar = $(this);
            var $gridNotFound = $('<div class="row-not-found-in-jig-grid" style="font-size:1em;padding:.5em;">No row containing the filter text.</div>');
            var count = $gridWithFilterToolbar.ncbigrid('getRowCount');

            if (parseInt(count) > 0) {
                $('.row-not-found-in-jig-grid').remove();
            } else {
                $('.row-not-found-in-jig-grid').remove();
                $gridWithFilterToolbar.after($gridNotFound);
            }
        });

        $maincontent.on('ncbigridfilterremoved', 'table', function (a, b) {
            $('.row-not-found-in-jig-grid').remove();
        });
    });
})(jQuery);

(function ($) {
    // Add a clear button
    // Read more at https://jira.ncbi.nlm.nih.gov/browse/HP-960#comment-3421832
    $.fn.addClearButtonToTextbox = function (options) {
        var defaults = {};
        var options = $.extend(defaults, options);
        var TAB_KEY = 9;

        return this.each(function () {
            var $this = $(this);
            var $btn = $('<a href="#" class="clear-btn">x</a>');
            var $cont = $('<div class="clear-btn-cont"></div>');

            $this.wrap($cont);
            $btn.insertAfter($this);

            var $p = $this.parent();
            $p.on('keyup', 'input', function (e) {
                var $btn = $p.find('.clear-btn');
                if ($this.val() !== "") {
                    $btn.show();
                } else {
                    $btn.hide();
                }
            });

            $p.on('keydown', 'input', function (e) {
                var $btn = $p.find('.clear-btn');
                if ($this.val() !== "") {
                    $btn.show();
                    if (e.keyCode == TAB_KEY) {
                        $btn.focus();
                        return false;
                    }
                }
            });

            $p.on('click', 'a', function (e) {
                var $t = $p.find('input[type="text"]');
                $t.val('').focus().trigger('keyup');
                $(this).hide();
                return false;
            });

        });
    }
})(jQuery);

(function ($) {
    $(function () {

        $.subscribe('ncbigrid-loaded', function (event) {
            console.info('ncbigrid-loaded');
        });

        $.subscribe('cmspageloadcompleted', function (event, $data) {
            console.info('cmspageloadcompleted');
        });

        // Tweak the jig-grid filter toolbar by adding
        // 1. placeholder to the filter textbox
        // 2. add a custom text to the label for the textbox
        // and finally call the $.addClearButtonToTextbox() on the textbox to add a clear button
        // data = {placeholder: 'text', caption: 'text', $tables: [$table]}
        $.subscribe('add-a-clear-button-to-jiggrid-filter-textbox', function (event, data) {
            console.info('add-a-clear-button-to-jiggrid-filter-textbox');
            var defaults = {
                placeholder: '',
                caption: 'Filter this table',
                $table: []
            };

            data = $.extend(defaults, data);

            var placeholder = data.placeholder,
                caption = data.caption,
                $tables = data.$tables;

            for (var i = 0; i < $tables.length; i++) {
                var $table = $tables[i];
                if (!($table instanceof jQuery)) {
                    $table = $($table);
                }
                var $container = $table.closest('.filterToolbar-exists');
                var $filterToolbar = $container.find('.ui-ncbigrid-filter-toolbar');

                // make the label bold
                $filterToolbar.find('label').text(caption).css('font-weight', 'bold');

                var $text = $filterToolbar.find('input[type=text][name="gridFilter"]');
                $text.attr('placeholder', placeholder).addClearButtonToTextbox();
            }
        });

    });
})(jQuery);

function getParamValue(paramName) {
    var filterText = "",
        params = document.location.search || [];

    if (params.length) {
        params = params.replace(/\?+(.*)/gi, "$1").split('&');

        if (params.length > 0) {
            for (var i = 0; i <= params.length; i++) {
                var parts = params[i].split('=');
                if (parts.length == 2 && parts[0].toLowerCase() == paramName) {
                    filterText = parts[1];
                }
                if (filterText !== "") {
                    break;
                }
            }
        }
    }
    return filterText;
}

// QuickStart Submit Menu
(function ($) {
    $(function () {
        var $selectMoreContainer = $('.select-more-options');
        $selectMoreContainer.on('change', '.select-more-options-p', function (e) {
            var $this = $(this);
            var $selOption = $this.find('option:selected');
            if (typeof $selOption.attr('data-more-options') !== 'undefined') {
                var $hasMoreOption = $($selOption.attr('data-more-options'));
                $hasMoreOption.show()
                    .removeAttr('disabled');
            } else {
                $selectMoreContainer.find('select[data-more-options]')
                    .hide()
                    .attr('disabled', 'disabled');
            }
        });


        $('#submit-data-button').on('click', function (e) {
            var $selOption = $('#submit-to').find('option:selected');
            var value = "";
            if (typeof $selOption.attr('data-more-options') !== 'undefined') {
                var $hasMoreOption = $($selOption.attr('data-more-options'));
                value = $hasMoreOption.val();
            } else {
                value = $selOption.val();
            }
            document.location.href = value;
            e.preventDefault();
        });

        $('#submit-to').trigger('change');
    });
})(jQuery);

function populate_analysis_tools_table() {
    var DEFAULT_GRID_OPTIONS = {
        filterToolbarIsCaseInsensitive: true,
        filterToolbarEnabled: true,
        isSortable: false
    };

    if (typeof GRID_OPTIONS !== 'undefined') {
        jQuery.extend(DEFAULT_GRID_OPTIONS, GRID_OPTIONS);
    }

    var $tables = jQuery('#analyze-page-content').find('.jig-ncbigrid');
    jQuery('#tutorial-table').ncbigrid(DEFAULT_GRID_OPTIONS);

    jQuery.publish('add-a-clear-button-to-jiggrid-filter-textbox', {
        $tables: $tables
    });
}

function setUpSubmitWizardPage() {
    var $container = jQuery(this),
        $table = $container.find('#submit-wizard');
    $table.find('th:last-child, td:last-child').hide();

    jQuery.publish('add-a-clear-button-to-jiggrid-filter-textbox', {
        $tables: [$table],
        'caption': 'I am submitting',
        'placeholder': 'mRNA, genome, plasmid, SNP, RNAseq, experiment, manuscript, genetic test...'
    });

    //If there is a param filter in the url, put in the jig-grid filter textbox
    var filter = getParamValue("filter");
    if (filter !== "") {
        var $gridFilterTextBox = jQuery('#submit-wizard-container .ui-ncbigrid-filter-toolbar input[name="gridFilter"]');
        $gridFilterTextBox.val(filter)
            .trigger('keyup');
    }
}

jQuery(function () {
    (function () {
        var $signIn = jQuery("#sign-in-checkstatus"),
            $signedIn = jQuery("#signed-in-checkstatus");
        if (isMyNCBIUserLoggedIn() === true) {
            $signIn.hide();
            $signedIn.show();
        } else {
            $signIn.show();
            $signedIn.hide();
        }
    })();
});

function populate_presentation_table() {

    var DEFAULT_GRID_OPTIONS = {
        sortColumn: 1,
        filterToolbarIsCaseInsensitive: true,
        filterToolbarEnabled: true
    };

    if (typeof GRID_OPTIONS !== 'undefined') {
        jQuery.extend(DEFAULT_GRID_OPTIONS, GRID_OPTIONS);
    }

    var $table = jQuery('#presentation-table').ncbigrid(DEFAULT_GRID_OPTIONS);

    jQuery.publish('add-a-clear-button-to-jiggrid-filter-textbox', {$tables: [$table]});
}
