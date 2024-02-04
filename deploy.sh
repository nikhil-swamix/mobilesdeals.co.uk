source $HOME/.nvm/nvm.sh
cd mobilesdeals.co.uk
git pull
bun run build
pm2 restart mobilesdeals.co.uk
exit
# ok