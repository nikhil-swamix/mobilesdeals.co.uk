source $HOME/.nvm/nvm.sh
cd mobilesdeals.co.uk
git pull
pnpm build      
pm2 restart all
exit
# ok