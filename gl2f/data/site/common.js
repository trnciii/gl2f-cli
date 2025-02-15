function addRetry(target, updator, onError){
  const maxRetries = 10;
  const retryDelay = 500;
  let retries = 0;
  target.addEventListener('error', () => {
    if(retries < maxRetries){
      retries++;
      console.warn(`Retrying ${target._src} (${retries}/${maxRetries})`);
      setTimeout(() => {
        updator(retries);
      }, retryDelay);
    }
    else{
      console.error(`Failed to load media ${target._src} after ${maxRetries} retries.`);
      onError();
    }
  });
}

function createVideoTile(src, displayName, width, notifier, observer){
  const video = document.createElement('video');
  video.controls = true;
  video.autoplay = true;
  video.muted = true;
  video.loop = true;
  video.width = width;
  video.title = displayName;
  video._src = src;

  addRetry(video,
    retries => {
      video.src = `${src}?retry=${retries}`;
      video.load();
    },
    ()=>notifier.error(`Failed to load video. See the log for more info.`));

  observer.observe(video);

  return video;
}

function tileMedia(mediaList, width, columns, showList, notifier)
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
    list.innerHTML = `<div style="padding:20px; background: pink;text-align:left;">${mediaList.map(i=>`<div class=list-item>${i.path}</div>`).join('')}</div>`

    element.appendChild(list);
    element.appendChild(document.createElement('br'));
  }

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if(!entry.isIntersecting)
      {
        return;
      }

      if(entry.target.tagName == 'IMG')
      {
        const img = entry.target;
        img.src = img._src;
        obs.unobserve(img);
      }
      else if (entry.target.tagName == 'VIDEO')
      {
        const video = entry.target;
        video.src = video._src;
        video.load();
        obs.unobserve(video);
      }
      else {
        console.warn(`[Observer] Unknown target ${entry.target.tagName}`);
      }
    });
  });

  mediaList.map(i =>
  {
    const src = `contents/${i.path}`;
    const ext = src.slice(src.lastIndexOf('.'));
    if([".jpeg", ".png"].indexOf(ext) > -1){
      const a = document.createElement('a');
      a.className += "tiledImage";
      a.setAttribute("data-group", "gallery");
      a.href = src;

      const img = document.createElement("img");
      img.style.width = `${itemWidth}px`;
      img.style.height = `${itemWidth}px`;
      img.style.objectFit = 'cover';
      img.style.backgroundColor = '#a5a5a5';
      img.style.boxShadow = 'inset 0 0 2px 1px white';
      img.title = i.displayName;
      img.loading = 'lazy';
      img._src = src;

      observer.observe(img);
      addRetry(img,
        retries => img.src = `${src}?retry=${retries}`,
        ()=>notifier.error(`Failed to load media. See the log for more info.`));

      img.addEventListener('load', ()=>{
        img.style.height = 'auto';
      });

      a.appendChild(img);
      return a;
    }
    else if([".mp4"].indexOf(ext) > -1){
      const a = document.createElement('a');
      a.className += 'tiledIframe';
      a.href = src;
      a.appendChild(createVideoTile(src, i.displayName, itemWidth, notifier, observer));
      return a;
    }
    else if([".mov"].indexOf(ext) > -1){
      return createVideoTile(src, i.displayName, itemWidth, notifier, observer);
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

class Notification {
  constructor(containerId = 'notificationContainer') {
    this.container = document.getElementById(containerId);
  }

  info(message)
  {
    console.log(message);
    this.show(message, 'info');
  }

  warn(message)
  {
    console.warn(message);
    this.show(message, 'warning');
  }

  error(message)
  {
    console.error(message);
    this.show(message, 'error', 5000);
  }

  show(message, type='info', duration=3000) {

    const notification = document.createElement('div');
    notification.classList.add('notification', type);
    notification.textContent = message;
    notification.style.opacity = '0';
    notification.style.transform = 'translateX(20px)';

    this.container.appendChild(notification);

    requestAnimationFrame(() => {
      notification.style.opacity = '1';
      notification.style.transform = 'translateX(0)';
    });

    setTimeout(() => {
      notification.style.opacity = '0';
      notification.style.transform = 'translateY(20px)';
      setTimeout(() => notification.remove(), 500);
    }, duration);
  }
}

function createFcArticleUrl(board, contentId)
{
  return `https://girls2-fc.jp/page/${board}/${contentId}`;
}

async function updateHostName(updator, fallback)
{
  return fetch(window.location.href).then(res =>{
    const hostName = res.headers.get('X-Server-Name');
    console.log(`updateHostName set ${hostName}`);
    updator(hostName);
  }).catch(_ => {
    console.log('updateHostName set default');
    fallback();
  });
}
