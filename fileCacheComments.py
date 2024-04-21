###################################################################################################        
# Displays an error message asking to create the json file
def errorPopup(message):
    # Show a message dialog
    hou.ui.displayMessage(message, title="Error", severity=hou.severityType.Error)

# Function to save comments to JSON file
def save_comments_to_json(json_file, comments_data):
    with open(json_file, 'w') as file:
        json.dump(comments_data, file, indent=4)

# Function to read comments from Houdini parameters
def readCommentsFromParm():
    node = hou.pwd()  # Get the current node
    comment_parameter = node.parm("commenttoadd")
    author_parameter = node.parm("author")
    version_parameter = node.parm("version")

    if comment_parameter is not None and author_parameter is not None and version_parameter is not None:
        comment_text = comment_parameter.evalAsString()
        author_name = author_parameter.evalAsString()
        version_number = version_parameter.evalAsInt()
        node_name = node.name()
        return comment_text, author_name, version_number, node_name
    else:
        return None, None, None, None

# Function to add comment to existing comments data
def addNewComments(existing_data, new_comment):
    existing_data['versions'].append(new_comment)
    return existing_data

# Function to read comments from JSON file for a specific node
def readFromJson(json_file, node_name):
    if not os.path.exists(json_file):
        # If the JSON file is missing, show a popup window
        errorPopup("The JSON file is missing. Please make sure it exists.")
        return None
    
    with open(json_file, 'r') as file:
        comments_data = json.load(file)
        node_comments = []
        for version_data in comments_data['versions']:
            if 'node_name' in version_data and version_data['node_name'] == node_name:
                node_comments.append(version_data)
        return node_comments

def saveCommentToDisk():
    # Specify path to save the file
    projectpath = hou.getenv("JOB") + "/"
    json_file = projectpath + "comments.json"

    # Read comments from Houdini parameters
    comment_text, author_name, version_number, node_name = readCommentsFromParm()

    if comment_text is not None and author_name is not None and version_number is not None and node_name is not None:
        # Check if json file exists
        if os.path.exists(json_file):
            # Load existing comments data from json file
            with open(json_file, 'r') as file:
                comments_data = json.load(file)
        else:
            # Create new file if json doesn't exist
            comments_data = {"scene_name": hou.hipFile.basename(), "versions": []}

        # Check if both comment text and author name are not empty
        if comment_text.strip() != "" and author_name.strip() != "":
            # Define json structure
            new_comment = {
                "comment_id": str(len(comments_data['versions']) + 1),
                "author": author_name,
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "comment_text": comment_text,
                "version_number": version_number,
                "node_name": node_name
            }

            # Add new comment
            updated_comments_data = addNewComments(comments_data, new_comment)

            # Save updated comments 
            save_comments_to_json(json_file, updated_comments_data)
        else:
            # Warning about empty comment and author
            errorPopup("No comment to add")
            pass

    # Read comments
    comments_data = readFromJson(json_file, node_name)
    return comments_data
    
# Function to set comment text to parameter when the data doesn't exist
def displayWhenNotFound(version_value):
    node = hou.pwd() 
    displaycomment_parameter = node.parm("displaycomment")

    # Set the message indicating no comments were found for the specified version
    if displaycomment_parameter is not None:
        displaycomment_parameter.set("No comments found for version: {}".format(version_value))
        
# Function to set comment text to parameter
def displayCommentsOnParms(comments):
    node = hou.pwd()
    displaycomment_parameter = node.parm("displaycomment")

    if displaycomment_parameter is not None:
        # Join comments with spacing between them
        formatted_comments = "\n\n".join(comments)

        # Set comments to display
        displaycomment_parameter.set(formatted_comments)
        
# Callback function triggered when the version slider moves
def selectOnVersionMovement():
    # Get the current node
    node = hou.pwd()
    
    # Locate json file
    projectpath = hou.getenv("JOB") + "/"
    json_file = projectpath + "comments.json"

    # Get the version slider parameter
    version_slider = node.parm("version")

    # Get the value of the version slider
    version_value = int(version_slider.eval())

    # Get the node name
    node_name = node.name()

    # Read comments from json file for the current node
    comments_data = readFromJson(json_file, node_name)

    if comments_data:
        # Find the comment data for the current version and node name
        matched_comments = []
        for version_data in comments_data:
            if version_data['version_number'] == version_value:
                comment_text = version_data['comment_text']
                author = version_data.get('author', 'Unknown Author')
                timestamp = version_data.get('timestamp', 'Unknown Timestamp')
                formatted_comment = "{} - {} ({})".format(comment_text, author, timestamp.replace('T', ' '))
                matched_comments.append(formatted_comment)

        # Sort matched comments by timestamp in descending order (most recent first)
        matched_comments.sort(key=lambda x: x.split(' (')[1], reverse=True)

        # If there are no matched comments, display not found message
        if not matched_comments:
            displayWhenNotFound(version_value)
            # Color the node red
            node.setColor(hou.Color((1, 0, 0)))
        else:
            # Set the matched comments to the displaycomment parameter with spacing between them
            displayCommentsOnParms(matched_comments)
            # Color the node green
            node.setColor(hou.Color((0, 1, 0)))
    else:
        # Display not found message
        displayWhenNotFound(version_value)