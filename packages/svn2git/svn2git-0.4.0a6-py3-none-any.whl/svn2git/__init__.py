__version__ = "0.4.0-alpha.6"
__all__ = ["__version__", "SVN2GitOptions", "GitMigrationHelper", "GitBranches"]

from svn2git.git import GitBranches, GitMigrationHelper
from svn2git.options import SVN2GitOptions
