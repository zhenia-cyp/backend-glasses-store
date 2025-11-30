import { useState, useEffect } from "react";
import styles from './Block.module.css';

export default function Block({baseTitle}) {
 //let title = "Block Component";
 console.log(baseTitle);
 const [title, setTitle] = useState(baseTitle);
 useEffect(() => {
    console.log("Component mounted");
    }, [title]);
  return (
    <div className={styles['base-block']}>
      <p>This is a block component</p>
      <button onClick={()=>{
        setTitle("") ;
      console.log(title)} }>clear</button>
      <h1>{title}</h1>
    </div>

  );
}
