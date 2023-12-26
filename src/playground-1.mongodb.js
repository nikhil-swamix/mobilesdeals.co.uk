use('mobilesdeals-co-uk');

let collection = db.getCollection('MasterCatalog');
let filter = {};

filter['Telcos:device_product_json.product_type'] = 'Mobile Phone';

collection.find(filter);
// collection.distinct('Telcos:device_product_json.product_type');
