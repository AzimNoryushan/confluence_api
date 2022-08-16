import flask
#import flask_cors
import json

app = flask.Flask(__name__)

@app.route('/')
@app.route('/advanced_inventory_dashboard/')
def index():
    dashboard_info = {
        'Dashboard Name': 'Advanced Inventory Dashboard', 
        'Insights': 
        [
            {
                'Name': 'Total Units', 
                'Views' : 'Product Final View', 
                'Drilldown' : [],
                'Template' : 'Metric (Number)',
                'Group By' : [],
                'Filter By' : [],
                'Calculate By' : ['SUM - On Hand']
            }, 
            {
                'Name': 'Total Volume', 
                'Views' : 'Product Final View',
                'Drilldown' : [], 
                'Template' : 'Metric (Number)',
                'Group By' : [],
                'Filter By' : [],
                'Calculate By' : ['SUM - Total Cubic Meters Used']
            }, 
            {
                'Name': 'Total Units and Volume by Warehouse', 
                'Views' : 'Product Final View',
                'Drilldown' : [],
                'Template' : 'Table',
                'Group By' : ['Warehouse Name'],
                'Filter By' : [],
                'Calculate By' : ['SUM - On Hand', 'SUM - Total Cubic Meters Used']
            },
            {
                'Name': 'Total Units and Volume by Client', 
                'Views' : 'Product Final View',
                'Drilldown' : [],
                'Template' : 'Table',
                'Group By' : ['Client Name'],
                'Filter By' : [],
                'Calculate By' : ['SUM - On Hand', 'SUM - Total Cubic Meters Used']
            },
            {
                'Name': 'Products with No Customs', 
                'Views' : 'Product Final View',
                'Drilldown' : [],
                'Template' : 'Table',
                'Group By' : ['Name+SKU', 'Client Name', 'Customs Description', 'Country Of Manufacture Id', 'Commodity Code Id'],
                'Filter By' : ['Has Customs = False'],
                'Calculate By' : []
            },
            {
                'Name': 'Products with No Volume', 
                'Views' : 'Product Final View',
                'Drilldown' : [],
                'Template' : 'Chart (Bar)',
                'Group By' : ['Name+SKU'],
                'Filter By' : ['Volume = False', 'On Hand != 0'],
                'Calculate By' : ['SUM - On Hand']
            },
            {
                'Name': 'Products with No Volume', 
                'Views' : 'Product Final View',
                'Drilldown' : [],
                'Template' : 'Chart (Bar)',
                'Group By' : ['Name+SKU'],
                'Filter By' : ['Volume = False', 'On Hand != 0'],
                'Calculate By' : ['SUM - On Hand']
            },
            {
                'Name': 'Products with No Barcode', 
                'Views' : 'Product Final View',
                'Drilldown' : [],
                'Template' : 'Chart (Bar)',
                'Group By' : ['Name+SKU'],
                'Filter By' : ['Has Barcode = False', 'On Hand != 0'],
                'Calculate By' : ['SUM - On Hand']
            },
            {
                'Name': 'Product Run Rate', 
                'Views' : 'Order Items Final View',
                'Drilldown' : [],
                'Template' : 'Chart (Bar)',
                'Group By' : ['Product Name+SKU'],
                'Filter By' : [],
                'Calculate By' : ['SUM - Quantity']
            },
            {
                'Name': 'Fast Moving Lines - Table', 
                'Views' : 'Order Items Final View',
                'Drilldown' : ['Fast Moving Lines - Chart'],
                'Template' : 'Table',
                'Group By' : ['Product Name+SKU', 'Client Name'],
                'Filter By' : [],
                'Calculate By' : ['SUM - Quantity']
            },
            {
                'Name': 'Slow Moving Lines - Table', 
                'Views' : 'Order Items Final View',
                'Drilldown' : ['Slow Moving Lines - Chart'],
                'Template' : 'Table',
                'Group By' : ['Product Name+SKU', 'Client Name'],
                'Filter By' : [],
                'Calculate By' : ['SUM - Quantity']
            },
            {
                'Name': 'Fast Moving Lines - Chart', 
                'Views' : 'Order Items Final View',
                'Drilldown' : [],
                'Template' : 'Table',
                'Group By' : ['Product Name+SKU'],
                'Filter By' : [],
                'Calculate By' : ['SUM - Quantity']
            },
            {
                'Name': 'Slow Moving Lines - Chart', 
                'Views' : 'Order Items Final View',
                'Drilldown' : [],
                'Template' : 'Table',
                'Group By' : ['Product Name+SKU'],
                'Filter By' : [],
                'Calculate By' : ['SUM - Quantity']
            },
            {
                'Name': 'Product Growth Rate - Table', 
                'Views' : 'Order Items Final View',
                'Drilldown' : ['Product Growth Rate - Chart'],
                'Template' : 'Table',
                'Group By' : ['Client Name' ,'Name+SKU', 'Current Week'],
                'Filter By' : [],
                'Calculate By' : ['SUM - This Week Quantity', 'SUM - Growth Rate']
            },
            {
                'Name': 'Product Growth Rate - Chart', 
                'Views' : 'Order Items Final View',
                'Drilldown' : [],
                'Template' : 'Chart (Column and Line)',
                'Group By' : ['Current Week'],
                'Filter By' : [],
                'Calculate By' : ['SUM - This Week Quantity', 'SUM - Growth Rate']
            }
        ], 
        'Filters': 
            ['Client Name', 
            'Warehouse Name', 
            'Product Name', 
            'SKU',
            'Client Short Name',
            'On Hand',
            'Product Name (SKU)',
            'Client Name',
            'Warehouse Name',
            'Order Status Name',
            'Order Date (ccyy/mm)',
            'Order Date',
            'Product Name',
            'Product SKU',
            'Client Short Name',
            ]
        }
    
    return flask.jsonify(dashboard_info)

@app.route('/dashboard_summary_test')
def dashboard_summary_test():
    dashboard_info = {
        'Dashboard Name': 'Dashboard Summary Test', 
        'Insights': 
        [
            {
                'Name': 'Clients - Aged Creditors', 
                'Views' : 'Access EzBuild - Clients Transactions', 
                'Drilldown' : ['Clients - Transaction Records'],
                'Template' : 'Stacked Column Chart',
                'Group By' : ['ClientName'],
                'Filter By' : ['ClientId != filter value', 'BalanceUnpaid != blank'],
                'Calculate By' : ['SUM - Days30', 'SUM - Days31To60', 'SUM - Days61To90', 'SUM - Days90Plus']
            }, 
            {
                'Name': 'Clients - Total Retention', 
                'Views' : 'Access EzBuild - Clients Transactions',
                'Drilldown' : [], 
                'Template' : 'Metric',
                'Group By' : [],
                'Filter By' : ['BalanceKey != filter value'],
                'Calculate By' : ['Total Retention ( SUM - LatestCumulativeRetention MINUS SUM - TransactionRetentionAmount)']
            }, 
            {
                'Name': 'Clients - Certified Balances &amp; Retentions', 
                'Views' : 'Access EzBuild - Clients Transactions',
                'Drilldown' : ['Clients - Certified Balances &amp; Retentions List', 'Clients - Transaction Records (Certified Only)'],
                'Template' : 'Stacked Column Chart',
                'Group By' : [],
                'Filter By' : ['ProjectName != filter value'],
                'Calculate By' : ['Total Retention ( SUM - LatestCumulativeRetention MINUS SUM - TransactionRetentionAmount)', 'Gross Certified (SUM - LatestCumulativeGrossCertified MINUS SUM - GrossCertifiedTransactionAmount)']
            },
            {
                'Name': 'Suppliers - Aged Balances', 
                'Views' : 'Access EzBuild - Suppliers Transactions',
                'Drilldown' : ['Suppliers - Aged Balances List', 'Suppliers - Transaction Records (Balances Only)'],
                'Template' : 'Stacked Column Chart',
                'Group By' : ['SupplierName'],
                'Filter By' : ['SupplierId != filter value', 'PaymentStatusDesc != Paid'],
                'Calculate By' : ['SUM - CurrentMonth', 'SUM - Month-1', 'SUM - Month-2', 'SUM - Month-3', 'SUM - Month-4', 'SUM - Month-5', 'SUM - BeforeMonth-5']
            }
        ], 
        'Filters': 
            ['Batch GL Date', 
            'Company', 
            'Financial Period', 
            'Last Financial Period End Date', 
            'Project', 
            'Transaction Date',
            'Test Field',
            'Test Field 2'
            ]
        }
    
    return flask.jsonify(dashboard_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)