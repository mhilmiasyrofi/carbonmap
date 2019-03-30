const fs = require('fs');
const readline = require('readline-sync');
require('colors');

const languages = fs.readdirSync('.')
  .filter(f => f !== 'en.json' && f.endsWith('.json'))
  .map(f => f.replace('.json', ''));

console.log('Languages you can translate: ' + languages.join(', ').green);
const language = readline.question('Which language do you want to translate: ');
if (!languages.includes(language)) {
  console.error((language + ' is not a translatable language!').red);
  return;
}

console.log();

const en = JSON.parse(fs.readFileSync('en.json'));
const other = JSON.parse(fs.readFileSync(language + '.json'));

function checkUntranslated(e, o, p) {
  if (typeof e === 'string') {
    if (o === undefined) {
      o = readline.question(p.slice(0, -1).blue + ' [' + e.green + ']: ');
      if (o === '') {
        o = e;
      }
    }
  } else {
    if (o === undefined) {
      o = {};
    }
    Object.keys(e).forEach(key => {
      o[key] = checkUntranslated(e[key], o[key], p + key + '.');
    });
  }
  return o;
}

fs.writeFileSync(language + '.json', JSON.stringify(checkUntranslated(en, other, ''), null, 4));
console.log('Finished!');
