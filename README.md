A webpage to show the projects you have open sourced in github. You can take a look to the [live demo](http://nekocode.cn/project-gallery).

## How to start

To make this webpage work, you have to have two files `ui_data.js` and `list_data.js` in the `data` subdirectory. The `ui_data.js` file needs to contain all the UI-related configurations, and the `list_data.js` file needs to contain all your github repostories's information. However, you can generate these two js files with the help of the `gen_data.sh` script which is in the root directory.

Before starting, you need to request a github [access token](https://github.com/settings/tokens) for the generator script. Because the generator script need to fetch your information from github. When you get the token string, write it into a text file in the root directory named `token`.

Now, you can excute `./gen_data.sh ui-js` command to generate the `ui_dat.js` file into the data directory. And then you can change configurations in it. The second step is to generate the `list_data.js` file. Firstly, excute `./gen_data.sh list-txt` command to generate a intermediate text file `list_data.txt` into the data directory. It contains a list of all your github repostories: 

```
// Category Name
Repository Name, Starts Count, Forks Count
...
```

You can make some tweaks to this list such as reorder items or insert some new categories. And after you finish your tweaks, excute `./gen_data.sh list-js` command to generate the final `list-data.js` file into the data directory. Now you can open the `index.html` to see the final effect.

## Example

Checkout to the branch [`mine`](https://github.com/nekocode/project-gallery/tree/mine) to see my personal example.
