
var Keywords = require('../model/keywordModel')

var Keywordcontroller = []

Keywordcontroller.listaPreconceito = () => {
    return Keywords
        .find({},{type_prejudice:1})
        .exec()
}

Keywordcontroller.listaVars = (tipo) => {
    return Keywords
    .find({type_prejudice:tipo},{"sociolinguistic_variables.pt":1, "type_prejudice":1})
    .exec()
}

Keywordcontroller.getKeywordByIdPt = (id) => {
    return Keywords
        .find({ "type_prejudice" : id },{"sociolinguistic_variables.pt":1})
        .exec()
}

Keywordcontroller.getKeywordByIdEn = (id) => {
    return Keywords
        .find({ "type_prejudice" : id },{"sociolinguistic_variables.en":1})
        .exec()
}



module.exports = Keywordcontroller