var FicheiroModel = require('../model/ficheiroModel')

var FicheiroController={};

/**
 * Lista todos os ficheiros na base de dados
 * Ordenado por id descendente
 * Id maior indica ficheiro analisado mais recentemente
 */
FicheiroController.listaFicheiros = () => {
    return FicheiroModel.find({},
                              {"header.title":1,
                               "header.owner":1,
                               "header.url":1,
                               "header.srcType":1,
                               "header.keywords":1,
                               "header.id":1,
                               "header.dateExtraction":1,
                               "header.datePosted":1,
                               "header.plataform":1,
                             })
                        .sort({"header.title":-1})
                        .exec()
}

FicheiroController.getFicheiroById = (id) => {
    return FicheiroModel.findOne({"header.id": id})
                        .exec()
}

FicheiroController.addFicheiro = (ficheiro) => {
    return FicheiroModel.create(ficheiro)
}

FicheiroController.removeFicheiro = (id) => {
    return FicheiroModel.findByIdAndDelete(id)
                        .exec()
}

module.exports = FicheiroController

