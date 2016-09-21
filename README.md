# devscripts

A collection of python scripts which are useful for iOS development.

# Usage

## build.py

Build the Xcode project with indicated parameters, it will use ios_builder.py and pgyer_uploader.py internally.

```sh
python build.py <command>
```

## generate_global_image_swift.py

Generate a swift code file named GlobalImage.swift, which is defining a enum for the image resources locate in Assets.xcassets.
Then the image resources can be referred in source code as enum value, to avoid of string typo.

```sh
python generate_global_image_swift.py
```
