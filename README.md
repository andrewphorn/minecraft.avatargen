minecraft.avatargen
===================

Avatar generator using minecraft-compatible skins as the input.

**It is not suggested that you use this for anything time-sensitive.** It is pretty slow and as such, vigorous caching should be used. In fact, it would probably be better overall if you didn't use this at all :)

Usage
-----

```python
import avatargen

avatargen.dim = 16
avatargen.getCompleteHead(avatargen.loadSkinFromURL('https://s3.amazonaws.com/MinecraftSkins/Notch.png')).save('Notch_head.png','PNG')

# Not the most straightforward but whatever.
```

**Note:** This is __not__ intended for the average user to use.
