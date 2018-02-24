A showcase of projects I have open sourced. You can take a look to the [live demo](http://nekocode.cn/project-gallery).

## How to start

The `index.js` need to read ui config and github repositories data from two files - `ui_data.js` and `list_data.js` in the data sub-directory. So you need to create this two files by the [`generator.py`](data/generator.py) firstly.

Before you start generating the two data js files. You need to request a new github [access token](https://github.com/settings/tokens) for the data generator. Because the data generator need to fetch your user and repositories info from github by using this token. Afater you get the new token, you need to excute `echo YOU_GITHUB_TOKEN > token` in the project root direcoty to write the token string into a new file named 'token' which the data-generator need.

Now, you can use `gen_data.sh` script (It's a shell script wrap of `generator.py`) to generate the `ui_data.js` and `list_data.js`. Firstly, excute `./gen_data.sh ui-js` to generate the template `ui_dat.js` into the data directory. This file include some ui config of the webpage:

```
var UI_DATA = {
    "title": ...,
    "github": ...,
    "description": ...,
    "footer": ...
}
```

You can change the values into what you want.

And then, excute `./gen_data.sh list-txt` to generate a intermediate file - `list_data.txt` into the data directory. It contains a list like below:

```
// Category Name
Repository Name, Starts Count, Forks Count
...
```

You can reorder these items or insert some new categories. After you finish your tweaks, excute `./gen_data.sh list-js` to generate the final `list-data.js`.

Finally, when you get both the `ui_data.js` and `list_data.js` files, the webpage can work. Open the `index.html` to see the effect.
