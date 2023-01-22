# duplicates
creates hard links for duplicated files between two directories.

**Important:** for creating the hard link the destination file must be previously deleted, be aware of that.

## ToDo
Initial approach is wrong: directories are uninmportant, they are only needed to delimit the set of files.

## Check first

- **Filesystem must support hardlinks**
- **All files must share same filesystem**

### Data structure
```
files = { md5: { inode: (path1, path2, ..., pathN), filesystem: filesystem_id } }
```

### Goal
One inode per md5 and filesystem, no matter how many paths are associated to them.
