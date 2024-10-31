// @target photoshop

"use strict";

/**
 * Script to batch rename PSD files based on hidden text layer content
 */

// Enable double clicking from Mac Finder or Windows Explorer
"target photoshop";

// Set preferences
app.preferences.rulerUnits = Units.PIXELS;
app.displayDialogs = DialogModes.NO;

// Prompt user for variable name
var variableName = prompt("Enter the variable name for the text layer:", "Output-Filename");
if (!variableName) variableName = "Output-Filename";

// Select folder containing PSD files
var inputFolder = Folder.selectDialog("Select folder containing PSD files");

if (inputFolder != null) {
    // Get all PSD files in the folder
    var fileList = inputFolder.getFiles("*.psd");
    
    if (fileList.length > 0) {
        for (var i = 0; i < fileList.length; i++) {
            try {
                // Open each PSD file
                var doc = app.open(fileList[i]);
                
                // Find the text layer with matching name
                var targetLayer = null;
                for (var j = 0; j < doc.artLayers.length; j++) {
                    if (doc.artLayers[j].name === variableName && 
                        doc.artLayers[j].kind === LayerKind.TEXT) {
                        targetLayer = doc.artLayers[j];
                        break;
                    }
                }
                
                if (targetLayer) {
                    // Get text content
                    var newName = targetLayer.textItem.contents;
                    
                    // Clean filename of invalid characters
                    newName = newName.replace(/[\/\\:*?"<>|]/g, "-");
                    
                    // Create new file path
                    var newPath = fileList[i].parent.fsName + "/" + newName + ".psd";
                    
                    // Save and close document
                    doc.saveAs(new File(newPath));
                    doc.close(SaveOptions.SAVECHANGES);
                    
                    // Delete original file if name changed
                    if (fileList[i].fsName !== newPath) {
                        fileList[i].remove();
                    }
                } else {
                    alert("Warning: Layer '" + variableName + "' not found in " + fileList[i].name);
                    doc.close(SaveOptions.DONOTSAVECHANGES);
                }
            } catch (err) {
                alert("Error processing " + fileList[i].name + ": " + err);
            }
        }
        alert("Processing complete!");
    } else {
        alert("No PSD files found in selected folder!");
    }
}