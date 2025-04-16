
export interface Winder {
    getUrl:()=>string
    getQuery(url?:string):Record<string,string>
    name:string
}

declare global {
    const winder:Winder
    function fetchContent(url:string):string
}
