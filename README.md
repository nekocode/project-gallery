A showcase of projects I have open sourced. You can take a look to the [live demo](http://nekocode.cn/project-gallery).

## How to start

Firstly, you need to request a new github [access token](https://github.com/settings/tokens) for the data-generator, so that the data-generator can fetch your user and repositories info from github. And then excute `echo YOU_GITHUB_TOKEN > token` in the project root direcoty to write the token string to a new file named 'token'.

Now, you can excute `./gen_data.sh txt` to generate the intermediate product 'data.txt' into the data directory. It contains a list like below:
```
// Category Name
Repository Name, Starts Count, Forks Count
...
```

You can reorder the items or insert new categories. After you finish your tweaks, excute `./gen_data.sh js` to generate the final corresponding 'data.js' file by your tweaked 'data.txt'.

Finally, the 'index.html' can work. 
