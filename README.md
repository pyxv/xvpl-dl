# xvpl-dl
an xvideos.com playlist downloader, utilises `youtube-dl` and `beautifulsoup` under the hood

#### features

- can download multiple playlists in one command
- can be run repeatedly and won't download duplicate files
- further customisation possible using `youtube_dl` options (see below)

## install

### pre-requisites

- `python3` (tested with `v3.9`)
- `pip`
- (optional) `ffmpeg`

clone this repository to somewhere (e.g. your preferred downloads folder), then install the required modules with `pip`

```sh
git clone https://github.com/pyxv/xvpl-dl ~/Downloads/xvideos
cd ~/Downloads/xvideos
pip install -r requirements.txt
```

## usage

run the script at a terminal, passing each playlist url as an argument

```sh
python xvpl-dl.py https://www.xvideos.com/favorite/52500297/casual https://www.xvideos.com/favorite/38755061/female_orgasm https://www.xvideos.com/favorite/37487709/123
```

#### note

- each playlist's videos will be downloaded into a directory named `<profile>-<playlist_name>` within the current working directory
- you can provide a custom download location using the variable `custom_dl_dir` in `xvpl-dl.py`
- video files are saved in the format `<video_name>-<id>.<ext>`
- you can specify/amend [`youtube_dl options`](https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L129-L279) in the `Playlist.download()` method
