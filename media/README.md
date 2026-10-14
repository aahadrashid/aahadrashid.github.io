# Project photographs

The photographs in this folder came from Aahad's Desktop `Portfolio` folder and selected image assets inside the supplied portfolio PDF. The source files remain in place.

To add another photo:

1. Copy the image into this folder with a short descriptive filename.
2. Add it to the correct project group in `content/media.json`.
3. Write a factual `alt` description and a concise `caption`.
4. Run `python build_site.py` from the website folder.

Example gallery entry:

```json
{
  "file": "robot-test.jpeg",
  "alt": "Aahad testing the robot on a competition field",
  "caption": "Testing the ring-handling mechanism."
}
```

For a new project gallery, add the project's slug as a new key in `content/media.json`, with a `cover`, `coverAlt`, and one or more titled `groups`. The generator checks that every referenced file exists.
