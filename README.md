## Houdini Comment Tracker

![toolgiffinal](https://github.com/markelv1/File-Cache-with-Comments/assets/166550328/aaea3888-6d14-4bea-bbe9-c56fd6307744)

## Description:

The Houdini Comment Tracker is a utility designed to streamline the process of managing comments and annotations within SideFX Houdini projects. It offers an intuitive interface for adding, retrieving, and displaying comments associated with different versions of nodes within a Houdini scene.

## Features:

- **Versioned Comments**: Easily attach comments to specific versions of nodes in your Houdini scene. Each comment includes details such as the author, timestamp, and associated node.
- **Node Coloring**: Nodes are color-coded to indicate whether comments exist for the selected version.
  ![color update](https://github.com/markelv1/File-Cache-with-Comments/assets/166550328/692624a0-eccb-4d5d-a23d-32f80a5b07db)
- **Interactive Comment Display**: Utilize a user-friendly interface to navigate through different versions of nodes and view associated comments directly within the Houdini interface.
- **JSON Data Storage**: Comments are stored in a JSON file format, ensuring compatibility and ease of access for sharing and collaboration across team members or projects.
- **Error Handling**: Alerts users when essential JSON files are missing, guiding them to create the necessary files for seamless comment tracking.
- **Customizable Display**: Tailor the presentation of comments to suit your preferences, with options for sorting, formatting, and displaying comments within the Houdini parameter interface.

## Usage:

- Install the Houdini Comment Tracker tool by pasting the otls folder under you Houdini preferences, usually under C:\Users\ "Username" \Documents\houdiniX.X\otls
- Under the tab menu the node is called Filecache More.
- Set up the JSON file by pressing Add Comment for storing comments.
- Add comments to specific nodes within your Houdini scene using the provided interface. This comments are added when pressing the Save to Disk button or if needed it is posible to add new ones with the Add Comment button.
- Navigate through different versions (with the version slider) to view associated comments and annotations.

**Reminder**: The comment.json file is saved under $JOB so is recomended to set project before using it. You will also need to fill both of the parameters Author and Comment to add in order to save the comments, if you don't and error will popup saying "No comment to add"
