
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

Keywordcontroller.adicionaKeyword = (params,body) => {
    console.log(params)
    console.log(body)
    
    const pt = "sociolinguistic_variables.pt."+params.id2
    const en = "sociolinguistic_variables.en."+params.id2
    
    if(body.pt_array){
        var queryParamPT = {}
        var bodyParamPT = {}
        bodyParamPT["$each"]=body.pt_array
        queryParamPT[pt] = bodyParamPT
        return Keywords
            .updateOne({"type_prejudice":params.id},{$push:queryParamPT},{$new:true})
    }
    
    if(body.en_array){
        var queryParamEN = {}
        var bodyParamEN = {}
        bodyParamEN["$each"]=body.en_array
        queryParamEN[en] = bodyParamEN
        return Keywords
            .updateOne({"type_prejudice":params.id},{$push:queryParamEN},{$new:true})
    }
    return Keywords
            .findOne()
            .exec()
}


module.exports = Keywordcontroller