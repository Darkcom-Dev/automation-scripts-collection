# Automation Scripts Collection - Version 1.0

This repository contains a variety of utility scripts, each designed to perform specific tasks. Some scripts focus on automating file and folder operations, such as recursive file renamers and recursive comparators. Others automate project-related tasks, like project setup and license management. There are also terminal utilities designed for use when Xorg is unavailable, including hex viewers, Markdown viewers (or `.ipynb` viewers), text encryptors, and more. Additionally, some scripts are focused on privacy (like PDF manipulation tools), while others handle tasks like texture manipulation.

Each script is designed to **perform a specific task**, should be an **executable Python script**, and, whenever possible, **avoid third-party dependencies**.

## Script Descriptions

- **base64-encriptor**: (Rename pending) Encrypts and decrypts text, useful for sending private messages.
- **console-higlighter**: Currently highlights Markdown text; planned future support for `.ipynb` files.
- **create-python-projects**: Sets up the folder structure for Python projects. Pairs well with the `licenser` script.
- **files-comparator**: Compares files in bulk to check if they are identical, even with different names. (Checksum comparator to be added)
- **img-to-text**: An OCR tool for extracting text from images, useful for creating lighter documentation from images.
- **licenser**: Helps you choose the right license based on the type of asset or project.
- **pdf-manipulator**: Splits or merges pages in a PDF, useful for consolidating documents into a single file.
- **project-renamer**: Renames files according to a naming convention for consistent project organization, applying kebab-case for common files and snake_case for scripts.
- **texture-ops**: Performs operations on textures for 3D games. Developed as a separate tool due to its growth in complexity.
- **view-hex-nes**: A terminal-based hex viewer for NES files, but can be used with any file type.

## How to Use

1. Clone the repository.
2. Select the scripts you are interested in.
3. Grant execution permissions to the selected scripts.
4. Move the files to a directory included in your `$PATH` environment variable.

---
