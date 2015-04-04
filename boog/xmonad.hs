import XMonad
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.EwmhDesktops
import XMonad.Util.EZConfig
import XMonad.Util.Run(spawnPipe, runInTerm)
import System.IO

myLayout = avoidStruts (tiled ||| Mirror tiled) ||| Full ||| tiled
    where
        -- partition screen into two panes
        -- start with 1 master window
        -- filling half the screen
        -- incremented by 3/100 on every resize
        tiled = Tall 1 (3/100) (1/2)

myTerminal = "urxvt"

main = do
    xmproc <- spawnPipe "/usr/bin/xmobar /home/daan/.xmobarrc"
    xmonad $ ewmh defaultConfig
        { terminal = myTerminal
        , borderWidth = 2
        , normalBorderColor = "#b8b8b8"
        , focusedBorderColor = "#ab4642"
        , workspaces = ["α", "β", "γ"]
        , layoutHook = myLayout
        , manageHook = manageDocks <+> manageHook defaultConfig
        , logHook = dynamicLogWithPP xmobarPP
            { ppOutput = hPutStrLn xmproc
            , ppTitle = xmobarColor "#a1b56c" "" . shorten 80
            , ppCurrent = xmobarColor "#f7ca88" "" . wrap "[" "]"
            , ppHidden = xmobarColor "#f7ca88" ""
            , ppHiddenNoWindows = xmobarColor "#b8b8b8" ""
            }
        , handleEventHook = handleEventHook defaultConfig <+> fullscreenEventHook
        }
        `additionalKeysP`
        [ ("M-w", spawn "chromium")
        , ("M-f", safeRunInTerm "" "ranger")
        , ("M-c", kill)
        , ("M-s", spawn myTerminal)
        ]

