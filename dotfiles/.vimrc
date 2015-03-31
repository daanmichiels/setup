execute pathogen#infect()

set nocompatible

syntax enable

set background=dark
" colorscheme solarized
colorscheme base16-default
set guifont=DejaVu_Sans_Mono:h10:cANSI

" line numbers
set number
set relativenumber

" search options
set incsearch
set hlsearch
set ignorecase
set smartcase

set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab

"backspace over everything in insert mode
set backspace=indent,eol,start

set encoding=utf-8
set fileencoding=utf-8

nnoremap ; :
nnoremap : ;

set hidden

filetype indent on

" source .vimrc files from working directories
set exrc
" but only allow secure commands in them
set secure

" better tab completion
set wildmenu

" spacebar as the leader
let mapleader = ' '

" easier moving between windows
nmap <leader>h   <C-w>h
nmap <leader>j   <C-w>j
nmap <leader>k   <C-w>k
nmap <leader>l   <C-w>l
" easier moving of windows
nmap <leader>H   <C-w>H
nmap <leader>J   <C-w>J
nmap <leader>K   <C-w>K
nmap <leader>L   <C-w>L
" easier closing of windows
" easer interchanging of windows
nmap <leader>c   <C-w>c
nmap <leader>x   <C-w>x
" toggling of NERDTree
" no remapping because : will get replaced
nnoremap <leader>f   :NERDTreeToggle<CR>
" easier execution of the macro q
nmap <leader>q   @q
" easier copy-paste
nmap <leader>p   "+p
nmap <leader>y   "+y
vmap <leader>y   "+y
nmap <leader>d   "+d
vmap <leader>d   "+d
" toggle gundo
nnoremap <leader>u   :GundoToggle<CR>
" browse recent files
nnoremap <leader>oo  :browse oldfiles<CR>

" run latexmk on the current tex file
function! RunLatexMk ()
    let originalwd = getcwd()
    echo originalwd
    silent !cmd.exe /c start /min /d %:p:h latexmk -pvc -pdf %:p
endfunction
command! LatexMk call RunLatexMk()

" inserts a boogie board pdf into the currect texfile
" index indicates which picture to insert,
" with index=0 referring to the most recent one,
"      index=1 referring to the one before that,
"      index=2 referring to the one before that,
" and so on
function! InsertBoogieIntoTex (...)
    let index = 0
    if a:0 > 0
        let index = a:1
    end
    let output = system("insert-boogie-into-tex " . shellescape(expand('%:p')) . " " . index)
    put =output
    "read !insert-boogie-into-tex shellescape(expand('%:p')) 0
    "write
endfunction
" when editing a tex file, :BoogieBoard is the insert-boogie-
" into-tex command
command! -nargs=? BoogieBoard call InsertBoogieIntoTex(<f-args>)

" disable semantic completion by YouCompleteMe for C++
" and C because I couldnt' get it to work properly
let g:ycm_filetype_specific_completion_to_disable = {'c': 1, 'cpp': 1}

" set location of swapfiles
" double slash makes vim base the swapfile name
" one the file's full path to preserve uniqueness
set directory=$HOME/vimfiles/swapfiles//
set directory=$HOME/vimfiles/backupfiles//
set directory=$HOME/vimfiles/undofiles//


