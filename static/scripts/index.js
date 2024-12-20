var authWin;
var authTimer;
var result_data;

function openAuthWin() {
    authWin = window.open('/authorize', 'Authorize', 'width=616,height=770');
    authTimer = setInterval( function() {
        if (authWin.closed) {
            clearInterval(authTimer);
            isAuthorized();
        }
    },
    1000 );
}

function isAuthorized() {
    let result = document.cookie.split(";")[document.cookie.split(";").length - 1].split("=")[1];
    if (result != null) {
        result = window.atob(result);
        result = result.replaceAll("'", "\"");
        result_data = JSON.parse(result);
        console.log("Authorized");

        document.getElementById("authButton").innerText = "Authorized";

        (async() => await getGuilds(result_data))();

        return true;
    }
    else {
        document.getElementById("authButton").innerText = "Unauthorized";
        return false;
    }
    
}

async function getGuilds(result_data) {
    let user_guilds = await fetch(
        "https://discord.com/api/v10/users/@me/guilds",
        {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + result_data["access_token"],
                "Content-Type": "application/json"
            }
        }
    ).then((response) => response.json());

    let bot_token = null;
    await fetch(
        "/fetch?bot_token",
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        }
    ).then(
        function (response) { return response.json() }
    ).then(
        (json) => { bot_token = json["BOT_TOKEN"] }
    );

    console.log(bot_token);

    let bot_guilds = await fetch(
        "https://discord.com/api/v10/users/@me/guilds",
        {
            method: "GET",
            headers: {
                "Authorization": "Bot " + bot_token,
                "Content-Type": "application/json"
            }
        }
    ).then(
        (response) => response.json()
    )

    bot_guilds = bot_guilds.map((x) => {return x.id;});

    let guild_select = document.getElementById("guild_select");

    for (let guild of user_guilds) {
        let guild_option = document.createElement("option");
        guild_option.value = guild.id;
        guild_option.innerText = guild.name;
        if (!bot_guilds.includes(guild.id)) {
            guild_option.disabled = true;
        }
        guild_select.appendChild(guild_option);
    }

    return "done";
}

function getCode(result) {
    let code = result.replace("b'", "").replace("'", "")
    document.cookie = "result=" + code;
    console.log(code);
}

function onSelectChange() {
    let select_div = document.getElementById("guild_select");
    select_div.disabled = true;
    let loading_div = document.getElementById("loading_div");
    loading_div.hidden = false;
    loading_div.classList.add("fadeMe");

    (async () =>  await fetchMutualResults(
        select_div.children[select_div.selectedIndex].value
    ));

}

async function fetchMutualResults(guild_id) {
    const mutuals = await fetch(
        "/fetch?mutuals&guild_id" + guild_id,
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        }
    ).then((response) => response.json());

    const mutual_servers = Object.keys(mutuals);

    for (let server in mutual_servers) {
        const current_guild = await fetch(
            "/fetch?guild&guild_id=" + guild_id,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        ).then((response) => response.json());

        const server = document.createElement("div");
        const server_pfp = document.createElement("img");
        server_pfp.src = "https://cdn.discordapp.com/icons/" + current_guild.id + "/" + current_guild.icon.key + ".webp";
        server_pfp.width = 32;
        server_pfp.height = 32;

        const server_name = document.createElement("h2");
        server_name.innerText = current_guild.name;

        server.appendChild(server_pfp);
        server.appendChild(server_name);

        for (let user in mutuals[server]) {
            const mutual_user = document.createElement("div");
            const mutual_user_pfp = document.createElement("img");
            mutual_user_pfp.src = user['avatar'];
            mutual_user_pfp.width = 32;
            mutual_user_pfp.height = 32;

            mutual_user.innerHTML.appendChild(mutual_user_pfp);
            mutual_user_name = document.createElement("div");
            mutual_user_global_name = document.createElement("p");
            mutual_user_username = document.createElement("p");
            mutual_user_global_name.innerText = user["global_name"];
            mutual_user_username.innerHTML = user["name"];

            mutual_user_name.appendChild(mutual_user_global_name);
            mutual_user_name.appendChild(document.createElement("br"));
            mutual_user_name.appendChild(mutual_user_username);

            mutual_user.appendChild(mutual_user_name);
            server.appendChild(mutual_user);
        }
    }
}