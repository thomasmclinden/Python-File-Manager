import re  # Import the regular expression module for pattern matching
import tkinter as tk
from tkinter import ttk


class File:
   def __init__(self, name, is_folder=False):
       self.name = name
       self.is_folder = is_folder
       self.children = []


   def add_file(self, child):
       if self.is_folder:  # if node is a folder
           self.children.append(child)  # add child to list
       else:  # else
           print("Error: This is not a folder.")  # if it is not a folder, a child cannot be added


   def __str__(self):
       return self.name


class Tree:
   def __init__(self):
       self.root = None


   def add_root(self, root_file):
       if isinstance(root_file, File):
           self.root = root_file
       else:
           print("Error: Invalid root file type.")


   def name_exists(self, filename, node = None):
       if node is None:
           node = self.root
       if node is None:
           return False  # The tree is empty


       if node.name == filename:
           return True


       if node.is_folder:
           for child in node.children:
               if self.name_exists(filename, child):
                   return True


       return False


   def display_tree(self, node=None, level=0):
       if node is None:
           node = self.root


       if node:
           print("  " * level + "|--", node)
           if node.is_folder:
               for child in node.children:
                   self.display_tree(child, level + 1)
               print()
       else:
           print("No folders to show")


   def delete_file(self, file_name, node=None, parent=None):
       if node is None:
           node = self.root


       if node:
           if not node.is_folder and node.name == file_name:
               if parent:
                   parent.children.remove(node)
                   return True
           elif node.is_folder:
               for child in node.children:
                   if self.delete_file(file_name, child, node):
                       return True
       return False


   def delete_folder(self, folder_name, node=None, parent=None):
       if node is None:
           node = self.root


       if node:
           if node.name == folder_name and node.is_folder:
               if parent is not None:
                   parent.children.remove(node)
               else:
                   self.root = None
               return True
           elif node.is_folder:
               for child in node.children:
                   if self.delete_folder(folder_name, child, node):
                       return True
       return False


   def move_file(self, file_name, target_folder_name, node=None, parent=None):
       if node is None:
           node = self.root
           parent = None


       if node:
           # First, check if the current node is the target folder
           if node.name == target_folder_name and node.is_folder:
               # Now we find and remove the file from its current location
               file_to_move = self.find_and_remove_file(file_name, self.root)
               if file_to_move:
                   node.add_file(file_to_move)  # Add it to the target folder
                   return True
               else:
                   return False
           else:
               # Recursively search through children
               for child in node.children:
                   if self.move_file(file_name, target_folder_name, child, node):
                       return True
       return False


   def find_and_remove_file(self, file_name, node, parent=None):
       if node:
           if not node.is_folder and node.name == file_name:
               if parent:
                   parent.children.remove(node)
                   return node
           elif node.is_folder:
               for child in node.children:
                   result = self.find_and_remove_file(file_name, child, node)
                   if result:
                       return result
       return None


   def copy_file(self, file_name, target_folder_name, node=None):
       if node is None:
           node = self.root


       if node:
           if node.name == target_folder_name and node.is_folder:
               # Find the file to copy
               file_to_copy = None
               for child in self.root.children:
                   file_to_copy = self.find_file(child, file_name)
                   if file_to_copy:
                       break


               if file_to_copy:
                   # Check if a file with the same name already exists in the target folder
                   copy_number = 1
                   while True:
                       copy_name = self.get_copy_name(file_name, copy_number)
                       if not self.name_exists(copy_name, node):
                           # If the copy name doesn't exist, create a copy-unique copies
                           node.add_file(File(copy_name))
                           return True
                       copy_number += 1
                   return True
               else:
                   print("Error: File not found.")
           elif node.is_folder:
               for child in node.children:
                   if self.copy_file(file_name, target_folder_name, child):
                       return True
       return False


   def find_file(self, node, file_name):
       if node:
           if node.name == file_name:
               return node
           elif node.is_folder:
               for child in node.children:
                   result = self.find_file(child, file_name)
                   if result:
                       return result
       return None


   def get_copy_name(self, file_name, copy_number):
       file_name_parts = file_name.split('.')
       file_name_base = '.'.join(file_name_parts[:-1])
       file_extension = file_name_parts[-1]
       return f"{file_name_base}({copy_number}).{file_extension}"
   def sort_files(self, node=None):
       if node is None:
           node = self.root
       if node:
           # If the node is a folder, sort its children
           if node.is_folder:
               node.children.sort(key=lambda x: x.name)
               for child in node.children:
                   self.sort_files(child)


class TreedisplayGUI:
   def __init__(self, file_manager):
       self.file_manager = file_manager


       self.root = tk.Tk()
       self.root.title("File Manager")
       # size of widget
       self.root.geometry("500x200")


       # setting windows as topmost
       self.root.attributes('-topmost', True)
       self.root.after_idle(self.root.attributes, "-topmost", False)


       self.tree = ttk.Treeview(self.root)
       self.tree.pack(expand=True, fill=tk.BOTH)


       self.display_treeview()


       self.root.mainloop()


   def display_treeview(self):
       if self.file_manager.root:
           self.build_tree(self.file_manager.root)
       else:
           self.tree.insert("", "end", text = "No folders to show. Please create folder to show.")


   def build_tree(self, node, parent=""):
       if node:
           item_id = self.tree.insert(parent, "end", text=node.name)
           if node.is_folder:
               for child in node.children:
                   self.build_tree(child, parent=item_id)
def display_menu():
   print("\nMenu")
   print("1. Add a folder\n2. Add a file\n3. Sort files\n4. Copy a file\n"
         "5. Move a file\n6. Delete a folder\n7. Delete a file\n8. Display the directory\n9. Exit")




def valid_name(name):
   # Checks if the name contains only allowed characters
   return re.match(r"^[a-zA-Z0-9_.\- ]+$", name) and not re.search(INVALID_CHARS_PATTERN, name)


if __name__ == "__main__":
   file_manager = Tree()


   while True:
       display_menu()
       option = input("Choose from the menu: ")


       # Define a regular expression pattern for matching invalid characters in file and folder names
       INVALID_CHARS_PATTERN = r'[\\/:"*?<>|]'  # Pattern for invalid characters


       if option == "1":
           while True:
               foldername = input("Enter the folder name: ")


               if not valid_name(foldername):
                   print("Error: Folder name can only contain alphanumeric characters and cannot contain \\ / : * ? \" < > |")


               elif foldername.upper() in ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6',
                                           'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6',
                                           'LPT7', 'LPT8', 'LPT9']:
                   print(f"Error: '{foldername}' is a reserved name in Windows.")


               elif file_manager.name_exists(foldername):
                   print("Error: folder already exists")
               else:
                   new_folder = File(foldername, is_folder=True)
                   if not file_manager.root:
                       file_manager.add_root(new_folder)
                       print("Root folder added successfully.")
                   else:
                       destination = input("Add folder to which folder (press Enter for root folder): ")
                       if destination == "":
                           file_manager.root.add_file(new_folder)
                           print("Folder added to root successfully.")
                       else:
                           folder = None
                           if file_manager.root:
                               folder = next(
                                   (child for child in file_manager.root.children if
                                    child.name == destination and child.is_folder),
                                   None)
                           if folder:
                               folder.add_file(new_folder)
                               print("Folder added to", destination, "successfully.")
                           else:
                               print("Destination folder not found.")
                   break


       elif option == "2":
           while True:
               file_name = input("Enter the file name: ")


               if not valid_name(file_name):
                   print("Error: Invalid Input! File name can only contain alphanumeric characters and cannot contain \\ / : * ? \" < > |")


               elif file_name.upper() in ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6',
                                          'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6',
                                          'LPT7', 'LPT8', 'LPT9']:
                   print(f"Error: '{file_name}' is a reserved name in Windows.")


               elif file_manager.name_exists(file_name):
                   print("Error: File already exists.")


               else:
                   folder_name = input("Add file to which folder: ")
                   folder = None
                   if file_manager.root:
                       folder = next(
                           (child for child in file_manager.root.children if
                            child.name == folder_name and child.is_folder),
                           None)
                   if folder:
                       folder.add_file(File(file_name))
                       print("File added successfully.")
                   else:
                       print("Error: Folder not found")
                       # display_menu()  # Return to the menu
                   break


       elif option == "3":
           file_manager.sort_files()
           print("Files sorted successfully.")
       elif option == "4":
           while True:
               file_name = input("Enter the file name: ")
               if not file_manager.name_exists(file_name):
                   print("Error: File not found. Please enter a valid file name.")
                   continue
               destination = input("Enter the target folder: ")
               folder = None
               def find_folder(node, folder_name):
                   if node:
                       if node.name == folder_name and node.is_folder:
                           return node
                       for child in node.children:
                           result = find_folder(child, folder_name)
                           if result:
                               return result


               if file_manager.root:
                   folder = find_folder(file_manager.root, destination)
               if folder:
                   file_manager.copy_file(file_name, folder.name)
                   print("File copied successfully.")
                   break
               else:
                   print("Destination folder not found.")


       elif option == "5":
           while True:
               file_name = input("Enter the file name: ")
               if not file_manager.name_exists(file_name):
                   print("Error: File does not exist. Please re-enter the file name.")
                   continue
               destination = input("Enter the target folder: ")
               if not file_manager.name_exists(destination):
                   print("Error: Target folder not found.")
                   continue
               if file_manager.move_file(file_name, destination):
                   print("File moved successfully.")
                   break
               else:
                   print("Failed to move the file. Please try again.")
                   break


       elif option == "6":
           folder_name = input("Enter the folder name: ")
           if file_manager.root:
               if file_manager.delete_folder(folder_name):
                   print("Folder deleted successfully.")
               else:
                   print("Folder not found.")


       elif option == "7":
           file_name = input("Enter the file name: ")
           deleted_file = file_manager.delete_file(file_name)
           if deleted_file:
                   print("File deleted successfully.")
           else:
                   print("File not found.")


       elif option == "8":
           file_manager.display_tree()
           TreedisplayGUI(file_manager)


       elif option == "9":
           print("\nProgram Ended")
           TreedisplayGUI(file_manager)
           break
       else:
           print("\nInvalid Input")
           pass



