import { useEffect, useState } from "react";

const useSize = () => {
  const [isOpen, setIsOpen] = useState(true);

  const handleResize = () => {
    if (window.innerWidth < 1265) {
      setIsOpen(false);
    } else {
      setIsOpen(true);
    }
  };

  useEffect(()=>{
    handleResize()
  },[])

  window.addEventListener("resize", handleResize);

  return isOpen;
};

export default useSize;
