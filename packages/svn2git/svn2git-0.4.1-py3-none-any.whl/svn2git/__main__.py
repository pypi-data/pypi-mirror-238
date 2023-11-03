import argparse
import logging
import sys

from svn2git import GitMigrationHelper, SVN2GitOptions

logger = logging.getLogger(__name__)

LOGGING_FORMAT_INFO = "%(asctime)s %(levelname)-6s %(message)s"
LOGGING_FORMAT_DEBUG = "%(asctime)s loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() L%(lineno)-4d %(message)s"


def main() -> None:
    """Main entry point for the application."""
    # Prepare
    parsed_args = parse(sys.argv[1:])
    git_migration_helper = GitMigrationHelper()

    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if parsed_args.verbose else logging.INFO,
        format=LOGGING_FORMAT_DEBUG if parsed_args.verbose else LOGGING_FORMAT_INFO,
    )

    # Perform
    if parsed_args.rebase:
        logger.info("Rebasing existing repository...")
        git_migration_helper.verify_working_tree_is_clean()
        branches = git_migration_helper.get_branches()
    elif parsed_args.rebase_branch:
        logger.info(f"Rebasing branch {parsed_args.rebase_branch}...")
        git_migration_helper.verify_working_tree_is_clean()
        branches = git_migration_helper.get_rebase_branch(branch_name=parsed_args.rebase_branch)
    else:
        logger.info("Cloning new repository...")
        git_migration_helper.clone(
            svn_url=parsed_args.svn_url,
            trunk_branch=parsed_args.trunk,
            branches=parsed_args.branches,
            tags=parsed_args.tags,
            metadata=parsed_args.metadata,
            no_minimize_url=parsed_args.no_minimize_url,
            root_is_trunk=parsed_args.root_is_trunk,
            authors_file_path=parsed_args.authors,
            exclude=parsed_args.exclude,
            revision=parsed_args.revision,
            username=parsed_args.username,
            password=parsed_args.password,
        )
        branches = git_migration_helper.get_branches()

    # Cleanup
    logger.info("Cleaning up...")
    git_migration_helper.fix_branches(branches=branches, rebase=parsed_args.rebase, trunk_branch=parsed_args.trunk)
    git_migration_helper.fix_tags(branches=branches)
    git_migration_helper.fix_trunk(branches=branches, rebase=parsed_args.rebase, trunk_branch=parsed_args.trunk)
    git_migration_helper.optimize_repository()

    # Finish
    logger.info("Done!")


def parse(to_parse_args: list[str]) -> SVN2GitOptions:
    """Parse command line arguments.

    Args:
        to_parse_args (list[str]): The command line arguments to parse.

    Returns
        SVN2GitOptions: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="svn2git",
        description="Migrate or rebase a SVN repository to Git",
        allow_abbrev=False,
        argument_default=argparse.SUPPRESS,
    )

    parser.add_argument("svn_url", metavar="SVN_URL", help="SVN repository URL")

    parser.add_argument(
        "--revision",
        metavar="START_REV:[END_REV]",
        help="Start importing from SVN revision START_REV; optionally end at END_REV",
    )

    parser.add_argument("--authors", metavar="AUTHORS_FILE", help="Path to file containing svn-to-git authors mapping")

    parser.add_argument(
        "--rebase", action="store_true", help="Instead of cloning a new project, rebase an existing one against SVN"
    )
    parser.add_argument("--rebase-branch", metavar="REBASE_BRANCH", help="Rebase specified branch")

    parser.add_argument("--username", help="Username for transports that needs it (http(s), svn)")
    parser.add_argument("--password", help="Password for transports that needs it (http(s), svn)")

    parser.add_argument(
        "--root-is-trunk",
        action="store_true",
        help="Use this if the root level of the repo is equivalent to the trunk and there are no tags or branches",
    )

    group_trunk = parser.add_mutually_exclusive_group()
    group_trunk.add_argument(
        "--trunk", metavar="TRUNK_PATH", default="trunk", help="Subpath to trunk from repository URL (default: trunk)"
    )
    group_trunk.add_argument("--no-trunk", action="store_true", help="Do not import anything from trunk")

    group_branches = parser.add_mutually_exclusive_group()
    group_branches.add_argument(
        "--branches",
        metavar="BRANCHES_PATH",
        action="append",
        default=["branches"],
        help="Subpath to branches from repository URL (default: branches); can be used multiple times",
    )
    group_branches.add_argument("--no-branches", action="store_true", help="Do not try to import any branches")

    group_tags = parser.add_mutually_exclusive_group()
    group_tags.add_argument(
        "--tags",
        metavar="TAGS_PATH",
        action="append",
        default=["tags"],
        help="Subpath to tags from repository URL (default: tags); can be used multiple times",
    )
    group_tags.add_argument("--notags", action="store_true", help="Do not try to import any tags")

    parser.add_argument(
        "--no-minimize-url",
        action="store_true",
        help="Accept URLs as-is without attempting to connect to a higher level directory",
    )
    parser.add_argument("--metadata", action="store_true", help="Include metadata in git logs (git-svn-id)")
    parser.add_argument(
        "--exclude",
        metavar="REGEX",
        action="append",
        help="Specify a Perl regular expression to filter paths when fetching; can be used multiple times",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Be verbose in logging -- useful for debugging issues"
    )

    parsed_args = parser.parse_args(args=to_parse_args)
    return SVN2GitOptions(**vars(parsed_args))


if __name__ == "__main__":
    main()
