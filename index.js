var zipper = require('adm-zip');

// build::
var zip = new zipper();

console.log('[zip]::build_contents_from_disk');
zip.addLocalFile('./README.md');
zip.addLocalFile('./params.json');
zip.addLocalFile('./lambda_function.py');
zip.addLocalFile('./requirements.txt');

var outfile = 'lambda-build.zip'
zip.writeZip(`./${outfile}`);
console.log('[zip]::artifact', outfile);
