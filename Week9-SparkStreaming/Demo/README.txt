To run this demo workbook you have to do a little preparation,
namely, you need to SSH to the cluster primary node and run a 
command.

These are the steps for Windows/Putty.  If you are using Mac, 
see notes below

1. If you have not already created a Key Pair, go to EC2 and 
then Key Pairs on the left nav.
2. Create key pair, upper right
3. Give the key pair a name, and select .ppk if you are using
Windows/Putty, or .pem otherwise.  Don't put spaces or special 
characters in the key name
4. When you create the key pair, it will download a file like
keypairname.pem or keypairname.ppk -- save that somewhere
5. When you create your EMR cluster, you will have the option of 
attaching a Key Pair.  Select the Key Pair you just created.
6. Start the cluster, and wait for the master node to be available
7. Go to the cluster dashboard, look at instances, click on the ID of
the primary instance. 
8. Find the public IP address and copy it.

Now start Putty.
a.  For host name (or IP address) use
         hadoop@<ip-address>
b.  Go to Connection -> SSH -> Auth -> Credentials
    You see a box "Private key file for authentication"
    Browse for the key file (.ppk) that you downloaded
    When you press Open a Putty window will open, 
       and you may get a security warning alert box.  Accept it.
c.  Now you are at the shell, and you enter this command
      sudo usermod -a -G hdfsadmingroup livy

There should be no output, just another shell prompt.
Close the window and you are good to go for using the cluster.

MAC differences
* You download a .pem file instead of .ppk
* Go to the location of the download, usually ~/Downloads
* There you will enter
     chmod 400 <mykeyname>.pem 
* Find the IP address of the primary node as in steps 6, 8, and 8 above.  
* In a terminal window you will then type
     ssh -i <mykeyname>.pem hadoop@<ip-address>
* That should give you the primary node shell prompt, and enter the command
  as in step c. above

