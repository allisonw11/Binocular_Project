const changePage = (page) =>{
    console.log("Changing page")
    window.location = `search${window.location.search.replace(/&page\=(\d+)/, '')}&page=${+page}`
  }
// window.location = url @ server.py "/search"
// .replace = replacing what's inside of (specific location using regex, '')-->sub the empty str with new ones