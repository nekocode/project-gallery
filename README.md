A webpage to show the projects you have open sourced in github. You can take a look to the [live demo](http://nekocode.cn/project-gallery).

## How to start

0. Request a github [access token](https://github.com/settings/tokens) for the generator script. Then excute `echo your_access_token > token`.

0. Install python module PyGithub `pip install pygithub`.

0. Excute `./gen_data.sh`. It will generate the `data.json` file into your `data` subdirectory.

0. Modify the `data.json`. For example, reorder or classify the repositories.

0. Now you can open the `index.html` to see the final effect.

## Example

Checkout to the branch [`mine`](https://github.com/nekocode/project-gallery/tree/mine) to see my personal example.
