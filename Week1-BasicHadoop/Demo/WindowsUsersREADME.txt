This issue applies to Windows users who are then running Linux through Docker.
Remember last night we were having problems with running our Python scripts
like split-lines in a shell pipeline.  For example if I tried

cat /data/textcorpora/* | split-lines

I would get an error, but

cat /data/textcorpora/* | python3 split-lines

would work.

It turns out the problem was due to the fact that I created those
scripts on my Windows machine, but I was using them in a Linux environment.
Files created in Windows (DOS Files) have different line ending characters than
files created in Linux (unix Files).

Now the problem is, just looking at the text, the difference in the line endings
is invisible!

You can avoid the problem by just creating all your files in Linux/Docker.  Even if you
store them in a Windows folder, they will still have the Unix line ending characters.

But I know some of you will be most comfortable using a text editor in Windows (like Notepad++)
for creating code you will run in Linux.  You can be careful to tell Notepad++ to use
unix line endings:  https://stackoverflow.com/questions/8195839/choose-newline-character-in-notepad

Also, there is a program you can install, dos2linux, that will convert a DOS file to a linux file:  https://lindevs.com/install-dos2unix-on-ubuntu
