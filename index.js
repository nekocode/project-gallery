var svgStart = '<svg aria-label="stars" class="octicon octicon-star" height="16" role="img" version="1.1" viewBox="0 0 14 16" width="14"><path fill-rule="evenodd" d="M14 6l-4.9-.64L7 1 4.9 5.36 0 6l3.6 3.26L2.67 14 7 11.67 11.33 14l-.93-4.74z"></path></svg>'

var svgFork = '<svg aria-label="forks" class="octicon octicon-repo-forked" height="16" role="img" version="1.1" viewBox="0 0 10 16" width="10"><path fill-rule="evenodd" d="M8 1a1.993 1.993 0 0 0-1 3.72V6L5 8 3 6V4.72A1.993 1.993 0 0 0 2 1a1.993 1.993 0 0 0-1 3.72V6.5l3 3v1.78A1.993 1.993 0 0 0 5 15a1.993 1.993 0 0 0 1-3.72V9.5l3-3V4.72A1.993 1.993 0 0 0 8 1zM2 4.2C1.34 4.2.8 3.65.8 3c0-.65.55-1.2 1.2-1.2.65 0 1.2.55 1.2 1.2 0 .65-.55 1.2-1.2 1.2zm3 10c-.66 0-1.2-.55-1.2-1.2 0-.65.55-1.2 1.2-1.2.65 0 1.2.55 1.2 1.2 0 .65-.55 1.2-1.2 1.2zm3-10c-.66 0-1.2-.55-1.2-1.2 0-.65.55-1.2 1.2-1.2.65 0 1.2.55 1.2 1.2 0 .65-.55 1.2-1.2 1.2z"></path></svg>'

// https://stackoverflow.com/a/2901298/5729581
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function addRepo(parentDom, name, stars, forks, lang, description, url) {
    var repoItem = document.createElement("li");
    repoItem.className = "repo-item";

    var header = '<h3><a href="' + url + '" target="_blank">' + name + '</a></h3>';
    var repoInfo = '<div class="repo-info"><span id="starts-info">' + svgStart + stars + '</span><span id="forks-info">' + svgFork + forks + '</span><span class="language Python">' + lang + '</span></div>';
    var repoDescription = '<p>' + description + '</p>';
    repoItem.innerHTML = header + repoInfo + repoDescription;

    parentDom.appendChild(repoItem);
}

function addPlaceHolderRepo(parentDom) {
    var repoItem = document.createElement("li");
    repoItem.className = "repo-item placeholder";
    parentDom.appendChild(repoItem);
}

function addCategory(parentDom, name) {
    var h2 = document.createElement("h2");
    h2.innerHTML = name;
    parentDom.appendChild(h2);
}

function setHeader(avatar, name, url) {
    document.getElementById("avatar").setAttribute("src", avatar);
    var userName = document.getElementById("user-name");
    userName.setAttribute("href", url);
    userName.innerHTML = name;
}

function loadData(user, items) {
    if (!user || !items) return;
    setHeader(user["avatar"], user["name"], user["url"])

    var content = document.getElementById("content");
    var item, type, placeHolderCount, repoCount = 0, listDom;
    function fillPlaceHolder() {
        if (repoCount > 0 && (repoCount % 4 > 1)) {
            placeHolderCount = 4 - (repoCount % 4);
            for (var j = 0; j < placeHolderCount; j++) {
                addPlaceHolderRepo(listDom);
            }
        }
        repoCount = 0;
    }
    for (var i = 0; i < items.length; i++) {
        item = items[i];
        type = item["type"];
        if (type == "category") {
            fillPlaceHolder();
            addCategory(content, item["name"]);

        } else if (type == "repo") {
            if (repoCount == 0) {
                listDom = document.createElement("ol");
                listDom.className = "repos-list";
                content.appendChild(listDom);
            }
            addRepo(listDom, item["name"], numberWithCommas(item["stars"]), numberWithCommas(item["forks"]), item["lang"], item["description"], item["url"]);
            repoCount++;
        }
    }
    fillPlaceHolder();
}

loadData(user_data, items_data);