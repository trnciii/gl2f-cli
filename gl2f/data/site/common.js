function tileMedia(mediaList, width, columns, showList)
{
  const itemWidth = width/columns;

  const element = document.createElement('center');

  if(showList)
  {
    const min = 250;

    const list = document.createElement('div');
    list.className = 'tile';
    list.style.marginTop = '20px';
    list.style.marginBottom = '20px';
    list.innerHTML = `<div style="padding:20px; background: pink;text-align:left;">${mediaList.map(i=>`<div class=list-item>${i}</div>`).join('')}</div>`

    element.appendChild(list);
    element.appendChild(document.createElement('br'));
  }

  mediaList.map(i =>
  {
    const src = `contents/${i}`;
    const ext = src.slice(src.lastIndexOf('.'));
    if([".jpeg", ".png"].indexOf(ext) > -1){
      const a = document.createElement('a');
      a.className += "tiledImage";
      a.setAttribute("data-group", "gallery");
      a.href = src;

      const img = document.createElement("img");
      img.src = src;
      img.width = itemWidth;
      img.title = i;
      img.loading = 'lazy';

      a.appendChild(img);
      return a;
    }
    else if([".mp4"].indexOf(ext) > -1){
      const a = document.createElement('a');
      a.className += 'tiledIframe';
      a.href = src;

      const video = document.createElement('video');
      video.controls = true;
      video.autoplay = true;
      video.muted = true;
      video.loop = true;
      video.width = itemWidth;
      video.title = i;

      const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry =>{
          if(entry.isIntersecting){
            video.src = src;
            video.load();
            obs.unobserve(video);
          }
        });
      });
      observer.observe(video);

      a.appendChild(video);
      return a;
    }
    else if([".mov"].indexOf(ext) > -1){
      const video = document.createElement('video');
      video.controls = true;
      video.autoplay = true;
      video.muted = true;
      video.loop = true;
      video.width = itemWidth;
      video.title = i;

      const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry =>{
          if(entry.isIntersecting){
            video.src = src;
            video.load();
            obs.unobserve(video);
          }
        });
      });
      observer.observe(video);

      return video;
    }
    else{
      alert(`Unknown media file: ${src}`);
      return document.createElement('div');
    }
  }).forEach(t =>
  {
    const i = document.createElement('div');
    i.className = 'tile';

    i.appendChild(t);
    element.appendChild(i);
  });

  return element;
}

function setupModaal()
{
  $('.tiledImage').modaal({
    type: 'image',
    hide_close: true,
  })
  $('.tiledIframe').modaal({
    type: 'iframe',
    hide_close: true,
  });
}