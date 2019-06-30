const axios = require('axios');
const Football = module.exports;

normalize = function(response) {
    return response.results.bindings.map(obj =>
        Object.entries(obj)
            .reduce((new_obj, [k,v]) => (new_obj[k] = v.value, new_obj),
                    new Object()));
};

async function execQuery(q){
    try{
        var encoded = encodeURIComponent(q);
        response = await axios.get("http://localhost:7200/repositories/football" + '?query=' + encoded);
        return(normalize(response.data));
    }
    catch(error) {
        return('ERRO: ' + error)
    }
}

Football.listCompetitions = async () => {
    const query = `PREFIX : <http://www.prc.di.uminho.pt/football#>
    select ?name ?comp where{
        ?comp a :Competition;
           :name ?name.
    }`;

    var res = await execQuery(query);
    return res;
};

Football.listCompetitionSeasons = (id) => {
    const query = `PREFIX : <http://www.prc.di.uminho.pt/football#>
    select ?name ?season where{
        :${id} :hasSeason ?season .
        ?season :season ?name.
    }`;

    return execQuery(query);

};

Football.listSeasonClassification = (id) => {
    const query = `PREFIX : <http://www.prc.di.uminho.pt/football#>
    select ?squadid ?pos ?squad ?pg ?win ?draw ?loss ?sc ?cg ?p where{
        :${id} :hasClassification ?class .
         ?class :classification ?pos;
                :squad_name ?squad;
                :played_games ?pg;
                :wins ?win;
                :draws ?draw;
                :losses ?loss;
                :scored_goals ?sc;
                :conceded_goals ?cg;
                :points ?p;
                :hasSquad ?squadid.
      }`;

    return execQuery(query);

};

Football.listSeasonSquad = (id) => {
    const query = `PREFIX : <http://www.prc.di.uminho.pt/football#>
    select ?p ?jnr ?pname ?pos where{
        :${id} :hasPlayer ?p .
         ?p :jersey_number ?jnr;
            :name ?pname;
            :position ?pos;
      }`;

    return execQuery(query);

};

Football.listPlayer = (id) => {
    const query = `PREFIX : <http://www.prc.di.uminho.pt/football#>
    select ?name ?bdate ?bplace ?nat ?h ?p ?jnr where{
        :${id}  :name ?name ;
                :birth_date ?bdate;
                :birth_place ?bplace;
                :nationality ?nat;
                :height ?h;
                :position ?p;
                :jersey_number ?jnr.
      }`;

    return execQuery(query);

};