const Ficheirocontroller = module.exports;
var Ficheiro = require('../model/ficheirocontroller')

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

