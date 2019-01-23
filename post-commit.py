#!/python

import sys
import os
import win32com.client as win32
import subprocess
import re
import html
import webbrowser
#import tempfile  #TODO: include attachment to the email else save as 

class CommitEmail():
  """
    Produces an email from the lastest git commit.  If exists, takes as input two files: 
      .git/hooks/hooks.approvallist
      .git/hooks/hooks.mailinglist
    that contain the list of approvers and other people that should get the email.  Else, 
    starts an email without a recipient list. 
  """
  def __init__(self):
    self.getrawdata()
  #      
  def getrawdata(self):
       self.raw = {}
       # get email addresses to send message to (re-write as hookconfig file)
       with open('.git/hooks/hooks.mailinglist', 'a+') as maillist, open('.git/hooks/hooks.approvallist', 'a+') as approvallist:
           maillist.seek(0)
           approvallist.seek(0)
           self.raw['notify']  = maillist.read()
           self.raw['request'] = approvallist.read()   
       #           
       #local and remote paths
       # making easier for browsers other than Chrome to open (Firefox and Explorer, need to check Firefox)
       self.raw['localPath'] = "file:///"+os.getcwd().replace('\\', '/')+"/"
       remotePathCode = subprocess.Popen('git config --get remote.origin.url', stdout=subprocess.PIPE)
       self.raw['remotePath'] = remotePathCode.stdout.read().decode('utf-8', 'replace').strip() 
       #
       # get commit history:
       LastCommit = subprocess.Popen('git log -p -1', stdout=subprocess.PIPE)
       self.raw['diffLog'] = LastCommit.stdout.read().decode('utf-8', 'replace').strip()
       #
       return self.raw
  #
  def HTMLLineformat(self,codeLine,divIndex,stl = {}):
      """
        transforms a line of the git diff in a line of HTML code
        TODO: close the <li>
      """
      output = codeLine
      #
      # Style options
      if stl == {}:
          stl['codeDivBackgroundColor'] = 'lightgrey'
          stl['codeDivFontFamily'] = 'Consolas'
          stl['codeDivDefaultFontColor'] = 'rgb(90, 90, 90)'
          stl['codeDivStyle'] = '"background-color:{0};font-family:{1};color:{2};max-height:409px;overflow:auto;"'.format(
               stl['codeDivBackgroundColor'], stl['codeDivFontFamily'], stl['codeDivDefaultFontColor'])
          stl['atColor'] = '"Dodgerblue"'  # '""' defaults to div font color.
          stl['removedCodeColor'] = '"red"'  # '"900C3F"'
          stl['newCodeColor'] = '"green"'
          stl['headColor'] = '"black"'
          stl['linkColor'] = '"Dodgerblue"'
      #
      #
      # note, divIndex starts at 0, after first @@ it becomes 1.
      if output.startswith('--- a/'):
          output = ''
      if output.startswith('+++ b/'):
          output = ''
      if output.startswith('+'):
          output = '<font color = ' + stl['newCodeColor'] + '>' + output + '</font>'
      #
      if output.startswith('-'):
          output = '<font color = ' + stl['removedCodeColor'] + '>' + output + '</font>'
      #
      if output.startswith('@'):
          # always start a div (of block code)
          output = '<font color = ' + stl['atColor'] + '>' + output + '</font>'
          if divIndex == 0:
              output = '<div style=' + stl['codeDivStyle'] + '>' + output
          divIndex = 1
      # note, will put a link to the file location
      if output.startswith('diff --git'):
          output = output.replace('diff --git', '')
          # strip removes whitespaces
          output = re.sub(r'a/.(.*?)b/', '', output).strip()
          # file locations:
          localFileRepoLink = '<a href = "{0}" style = "color:Gray">Local File</a>'.format(
              self.raw['localPath'] + output)
          if self.raw['remotePath'] != '/':
              remoteFileRepoLink = ', <a href = "{0}" style = "color:Gray">Remote File</a>'.format(
                  self.raw['remotePath'] + output)
          else:
              remoteFileRepoLink = ''
          if divIndex == 0:
              output = '<br><br><li> <em><font color = ' + stl['headColor'] + \
                  ' size = 4> File Changed: ' + output + '</font></em>'
          else:
              output = '</div><br><br><li> <em><font color = ' + stl['headColor'] + \
                  ' size = 4> File Changed: ' + output + '</font></em>'
              divIndex = (divIndex + 1) % 2
          # include link to file
          output = output + \
              '<br>[ {0} {1} ]'.format(localFileRepoLink, remoteFileRepoLink)
      return [output, divIndex]
  #
  def gitdiffToHTML(self):
      """
        transform git diff log into HTML
        TODO:once started html (html.escape) should make sure it is always htlm
      """  
      diffLog = self.raw['diffLog'].replace('\r', '').split('\n')
      divIndex = 0
      diffHTML = []
      for x in diffLog:
          output, divIndex = self.HTMLLineformat(html.escape(x), divIndex) 
          diffHTML.append(output)
      #
      diffHTML.insert(3, 'Local Path: <a href = "{0}" style = "color:Gray">'.format(
          self.raw['localPath']) + self.raw['localPath'] + '</a>')
      if self.raw['remotePath'] != '/':
          diffHTML.insert(4, 'Remote Path: <a href = "{0}" style = "color:Gray">'.format(
              self.raw['remotePath']) + self.raw['remotePath'] + '</a>')
      #fix the ending of the HTML file     
      endDiv = ''
      if divIndex == 1:
          divIndex = 0
          endDiv = '</div>'
      #
      diffHTML = '<ol>' + '<br>'.join(diffHTML) + endDiv + '</ol>'
      #
      # cosmetic - assure code is closer by a line to its filename block than to the next filename block
      diffHTML = diffHTML.replace('<br><br><br><div', '<br><br><div')
      #
      return diffHTML
    #
  def Email(self,mailserver,send=0):
        """
          Start an email or send it.  
          if no server is provided, open the html.
          TODO: include the output as attachement, include other email (smtp)
        """  
        if mailserver == 'outlook':
          #Start email ##################################
          os.startfile("outlook")
          outlook = win32.Dispatch('outlook.application')
          #
          #start mail
          mail = outlook.CreateItem(0)
          #
          #recipients
          all = self.raw['notify']+";"+self.raw['request']
          all = ";".join(list(set(all.split(";"))))
          mail.To = all
          #
          mail.Subject = '[[Committed Code Summary]]'
          mail.HtmlBody = self.gitdiffToHTML()
          #
          #attachment = tempfile.NamedTemporaryFile(   mode = 'w+t', suffix = '.txt')
          # attachment.writelines(diffHTML)
          #mail.Attachments.Add(Source = attachment.name)
          #
          if send == 0:
              mail.Display(True)
          else:
            mail.send()
        else:
            html = '<html>' + self.gitdiffToHTML() +'</html>'
            path = os.path.abspath('temp.html')
            url = 'file://' + path
            with open(path, 'w') as f:
                f.write(html)
            webbrowser.open(url)
      
      
print("\n", "****** Starting Post-Commit Hook ******")

CommitEmail().Email('outlook', send = 0 )

print("****** End of Post-Commit Hook ******", "\n")