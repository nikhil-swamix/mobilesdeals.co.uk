git pull
# source pm2

source $HOME/.nvm/nvm.sh
pnpm build      
pm2 restart all