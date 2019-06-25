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
                               "_id":1,
                               "header.dateExtraction":1,
                               "header.datePosted":1,
                               "header.plataform":1,
                             })
                        .exec()
}

FicheiroController.getFicheiroById = (id) => {
    return FicheiroModel.findOne({_id: id})
                        .exec()
}

//Esta função está funcional
FicheiroController.getFicheiroCount = () => {
    return FicheiroModel.countDocuments()
                        .exec()
}

FicheiroController.addFicheiro = (obj) => {
    return FicheiroModel.create(obj)
}

FicheiroController.removeFicheiro = (id) => {
    return FicheiroModel.findByIdAndDelete(id)
                        .exec()
}

module.exports = FicheiroController

