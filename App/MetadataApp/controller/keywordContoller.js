const Keywordcontroller = module.exports;
var Keyword = require('../model/keywordController')

Ficheirocontroller.NomeFicheiros = () => {
    return Ficheiro
        .find({},{titulo:1})
        .exec()
}

Ficheirocontroller.ficheiro = (titulo) => {
    return Ficheiro
        .find({titulo:titulo})
        .exec()
}