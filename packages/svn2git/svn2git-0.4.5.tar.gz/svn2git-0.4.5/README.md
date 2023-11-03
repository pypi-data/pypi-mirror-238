# svn2git CLI tool

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=helmergmbh_svn2git&metric=alert_status&token=8e09167190c0feda223224196407a3f60caeed86)](https://sonarcloud.io/summary/new_code?id=helmergmbh_svn2git)

_svn2git_ is a tiny utility for migrating projects from Subversion to Git
while keeping the trunk, branches and tags where they should be. It uses
git-svn to clone a SVN repository and does some clean-up to make sure
branches and tags are imported in a meaningful way, and that the code checked
into main ends up being what's currently in your SVN trunk rather than
whichever SVN branch your last commit was in.

Examples
--------

Say I have this code in SVN:

    trunk
      ...
    branches
      1.x
      2.x
    tags
      1.0.0
      1.0.1
      1.0.2
      1.1.0
      2.0.0

git-svn will go through the commit history to build a new git repo. It will
import all branches and tags as remote SVN branches, whereas what you really
want is git-native local branches and git tag objects. So after importing this
project I'll get:

    $ git branch
    * main
    $ git branch -a
    * main
      1.x
      2.x
      tags/1.0.0
      tags/1.0.1
      tags/1.0.2
      tags/1.1.0
      tags/2.0.0
      trunk
    $ git tag -l
    [ empty ]

After svn2git is done with your project, you'll get this instead:

    $ git branch
    * main
      1.x
      2.x
    $ git tag -l
      1.0.0
      1.0.1
      1.0.2
      1.1.0
      2.0.0

Finally, it makes sure the HEAD of main is the same as the current trunk of
the SVN repo.

## Prerequisites

Make sure to install:

- Python >= 3.11
- Git and git-svn

## Install

To install:

```bash
pip install svn2git
```

## Usage

### Initial Conversion

There are several ways you can create a git repo from an existing
SVN repo. The differentiating factor is the SVN repo layout. Below is an
enumerated listing of the varying supported layouts and the proper way to
create a git repo from a SVN repo in the specified layout.

1. The SVN repo is in the standard layout of (trunk, branches, tags) at the
   root level of the repo.

        $ svn2git http://svn.example.com/path/to/repo

2. The SVN repo is NOT in standard layout and has only a trunk and tags at the
   root level of the repo.

        $ svn2git http://svn.example.com/path/to/repo --trunk dev --tags rel --no-branches

3. The SVN repo is NOT in standard layout and has only a trunk at the root
   level of the repo.

        $ svn2git http://svn.example.com/path/to/repo --trunk trunk --no-branches --no-tags

4. The SVN repo is NOT in standard layout and has no trunk, branches, or tags
   at the root level of the repo. Instead, the root level of the repo is
   equivalent to the trunk and there are no tags or branches.

        $ svn2git http://svn.example.com/path/to/repo --root-is-trunk

5. The SVN repo is in the standard layout, but you want to exclude the massive
   doc directory and the backup files you once accidentally added.

        $ svn2git http://svn.example.com/path/to/repo --exclude doc --exclude '.*~$'

6. The SVN repo actually tracks several projects, and you only want to migrate
   one of them.

        $ svn2git http://svn.example.com/path/to/repo/nested_project --no-minimize-url

7. The SVN repo is password protected.

        $ svn2git http://svn.example.com/path/to/repo --username <<user_with_perms>>

   If this doesn't cooperate, and you need to specify a password on the command-line:

        $ svn2git http://svn.example.com/path/to/repo --username <<user_with_perms>> --password <<password>>

8. You need to migrate starting at a specific SVN revision number.

        $ svn2git http://svn.example.com/path/to/repo --revision <<starting_revision_number>>

9. You need to migrate starting at a specific SVN revision number, ending at a specific revision number.

        $ svn2git http://svn.example.com/path/to/repo --revision <<starting_revision_number>>:<<ending_revision_number>>

10. Include metadata (git-svn-id) in git logs.

        $ svn2git http://svn.example.com/path/to/repo --metadata

The above will create a git repository in the current directory with the git
version of the SVN repository. Hence, you need to make a directory that you
want your new git repo to exist in, change into it and then run one of the
above commands. Note that in the above cases the trunk, branches, tags options
are simply folder names relative to the provided repo path. For example if you
specified trunk=foo branches=bar and tags=foobar it would be referencing
http://svn.example.com/path/to/repo/foo as your trunk, and so on. However, in
case 4 it references the root of the repo as trunk.

### Repository Updates

There is a feature to pull in the latest changes from SVN into your
git repository created with svn2git. This is a one way sync, but allows you to use svn2git
as a mirroring tool for your SVN repositories.

The command to call is:

        $ cd <EXISTING_REPO> && svn2git --rebase

### Authors

To convert all your SVN authors to git format, create a file somewhere on your
system with the list of conversions to make, one per line, for example:

    phelmer = Pascal Helmer <pascal@not-your-mind.de>
    stnick = Santa Claus <nicholas@lapland.com>

Then pass an _authors_ option to svn2git pointing to your file:

    $ svn2git http://svn.example.com/path/to/repo --authors ~/authors.txt

If you need a jump start on figuring out what users made changes in your
SVN repositories the following command sequence might help. It grabs all
the logs from the SVN repository, pulls out all the names from the commits,
sorts them, and then reduces the list to only unique names. So, in the end
it outputs a list of usernames of the people that made commits to the SVN
repository which name on its own line. This would allow you to easily
redirect the output of this command sequence to `~/authors.txt` and have
a very good starting point for your mapping.

    $ svn log --quiet | grep -E "r[0-9]+ \| .+ \|" | cut -d'|' -f2 | sed 's/ //g' | sort | uniq

Or, for a remote URL:

    $ svn log --quiet http://path/to/root/of/project | grep -E "r[0-9]+ \| .+ \|" | cut -d'|' -f2 | sed 's/ //g' | sort | uniq

### Debugging

If you're having problems with converting your repository, and you're not sure why,
try turning on verbose logging. This will print out more information from the
underlying git-svn process.

You can turn on verbose logging with the `-v` or `--verbose` flags, like so:

    $ svn2git http://svn.yoursite.com/path/to/repo --verbose

### Options Reference

    $ usage: svn2git [-h] [--revision START_REV:[END_REV]]
               [--authors AUTHORS_FILE] [--rebase]
               [--rebase-branch REBASE_BRANCH]
               [--username USERNAME] [--password PASSWORD]
               [--root-is-trunk] [--trunk TRUNK_PATH | --no-trunk]
               [--branches BRANCHES_PATH | --no-branches]
               [--tags TAGS_PATH | --notags] [--no-minimize-url]
               [--metadata] [--exclude REGEX] [-v]
               SVN_URL

    Migrate or rebase a SVN repository to Git

    positional arguments:
        SVN_URL                         SVN repository URL

    options:
        -h, --help                      show this help message and exit
        --revision START_REV:[END_REV]  Start importing from SVN revision START_REV; optionally end at END_REV
        --authors AUTHORS_FILE          Path to file containing svn-to-git authors mapping
        --rebase                        Instead of cloning a new project, rebase an existing one against SVN
        --rebase-branch REBASE_BRANCH   Rebase specified branch
        --username USERNAME             Username for transports that needs it (http(s), svn)
        --password PASSWORD             Password for transports that needs it (http(s), svn)
        --root-is-trunk                 Use this if the root level of the repo is equivalent to the trunk and
                                        there are no tags or branches
        --no-minimize-url               Accept URLs as-is without attempting to connect to a higher level directory
        --metadata                      Include metadata in git logs (git-svn-id)
        --exclude REGEX                 Specify a Perl regular expression to filter paths when fetching; can be used
                                        multiple times
        -v, --verbose                   Be verbose in logging -- useful for debugging issues

### FAQ

1. Why don't the tags show up in the main branch?

   The tags won't show up in the main branch because the tags are actually
   tied to the commits that were created in SVN when the user made the tag.
   Those commits are the first (head) commit of branch in SVN that is
   associated with that tag. If you want to see all the branches and tags
   and their relationships in gitk you can run the following: gitk --all

   For further details please refer to FAQ #2.

2. Why don't you reference the parent of the tag commits instead?

   In SVN you are forced to create what are known in git as annotated tags.
   It just so happens that SVN annotated tags allow you to commit change
   sets along with the tagging action. This means that the SVN annotated tag
   is a bit more complex than just an annotated tag it is a commit which is
   treated as an annotated tag. Hence, for there to be a true 1-to-1 mapping
   between Git and SVN we have to transfer over the SVN commit which acts as
   an annotated tag and then tag that commit in git using an annotated tag.

   If we were to reference the parent of this SVN tagged commit there could
   potentially be situations where a developer would check out a tag in git
   and the resulting code base would be different from if they checked out
   that very same tag in the original SVN repo. This is only due to the fact
   that the SVN tags allow changesets in them, making them not just annotated
   tags.

## Development

### Prerequisites

Make sure to install:

- Python >= 3.11
- Poetry >= 1.6.1
- Git and git-svn
- Docker and docker-compose

### Install

Run:

```bash
poetry install
```

### Linting and typechecking

Setup pre-commit hooks:

```bash
poetry run pre-commit install
```

Run on all files:

```bash
poetry run pre-commit run -a
```

### Testing

Run tests with coverage report:

```bash
poetry run pytest
```

or run in watch mode:

```bash
poetry run pytest-watch -n
```

## Documentation

We are using Sphinx with the ReadTheDocs html theme.

You have the following ways to run a live reloading server to develop this documentation

- Run `poetry run python docs/docs_livereload.py`
- Run `docker compose up --build docs`

Both will run a webserver listing on http://localhost:5500 and will automatically rebuild the documentation (and
reloading the website inside your browser) if a file in docs or newtron_cdc directory changes.

(Third option would be to manually call `make html` or `./make.bat html` inside the docs directory.)
