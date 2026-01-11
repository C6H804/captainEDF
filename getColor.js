const getToday = async () => {
    const response = await fetch("https://www.api-couleur-tempo.fr/api/jourTempo/today");
    const data = await response.json();
    return data.libCouleur;
}

const getTomorrow = async () => {
    const response = await fetch("https://www.api-couleur-tempo.fr/api/jourTempo/tomorrow");
    const data = await response.json();
    return data.libCouleur;
}

const init = async () => {
    const today = await getToday();
    const tomorrow = await getTomorrow();
    // console.log("Couleur Tempo du jour :", today);
    // console.log("Couleur Tempo de demain :", tomorrow);
    // console.log(JSON.stringify([today, tomorrow]));
    console.log(today + " " + tomorrow);
}

init();