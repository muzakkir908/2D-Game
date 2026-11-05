# Note About AI Use

> **Please read and edit this note before you submit.** Your school may have rules about using AI tools, and it may ask you to explain how you used them. This note only lists facts about how the project files were made. Change it so it matches your own work and your school's rules.

## How the files in this project were made

This project was made with the help of an AI assistant (Claude, made by Anthropic), working from a detailed brief written by the student.

The AI assistant:
- wrote the game concept, rules and the other documents,
- wrote the Python programs in `tools/`, which draw all the pixel art, maps and screens,
- designed the level and wrote the level notes,
- made the HTML prototype,
- built the Figma prototype through Figma's plugin API.

The pixel art was not drawn by hand in a drawing program. It was written as text maps and code (see `How_To_Remake_The_Files.md`), and then turned into PNG files.

## What was checked

- The HTML prototype was opened in a browser by an automated test. Every button link was clicked and checked, and no errors were found.
- The Figma prototype links were read back from the Figma file and all of them point to the right screens. They were **not** clicked through by hand in Figma's Present mode.
- All the files were made again from the `tools/` scripts at the end, to make sure they match the scripts.

## Space for your own notes

*(Add here what you did yourself, for example: your ideas, the choices you made, the changes you asked for, and what you checked or changed by hand.)*
