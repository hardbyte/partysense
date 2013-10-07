# Partysense Developer Documentation

The technology behind the online collaborative music
website **[partysen.se][1]**.

## Repository Structure

- **PartySenseApp**: Code for the android application.
- **PartySenseAppiOS**: Code for the iOS application.
- **PartySenseSync**: Code for a standalone desktop application.
- **PartySenseWebBackend**: Google App Engine Server for partysenseapp.appspot.com
- **PartySenseWebFrontend**: Web Application for the partysen.se website

## Branches

Note we are using [gitflow][2], **master** should contain only stable
code. Develop is used for the day to day, deployements should always
happen off master. Large chunks of work get done in **feature branches**.

  [1]: http://partysen.se
  [2]: http://nvie.com/posts/a-successful-git-branching-model/