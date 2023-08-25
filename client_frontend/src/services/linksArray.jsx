import {
  AiFillHome,
  AiFillShop,
  AiFillNotification,
  AiFillSetting,
  AiFillShopping,
} from "react-icons/ai";
import { BsFillPeopleFill } from "react-icons/bs";
import { MdReviews } from "react-icons/md";
import { FiLogOut } from "react-icons/fi";
import { BiSolidUser, BiCommentError } from "react-icons/bi";

export const linksNav = [
  {
    label: "Inicio",
    to: "/",
    icon: <AiFillHome />,
  },
  {
    label: "Marketplace",
    to: "/marketplace",
    icon: <AiFillShop />,
  },
  {
    label: "Foro",
    to: "/foro",
    icon: <BsFillPeopleFill />,
  },
  {
    label: "Reseñas",
    to: "/reseña",
    icon: <MdReviews />,
  },
  {
    label: "Notificaciones",
    to: "/notificaciones",
    icon: <AiFillNotification />,
    number: 0,
  },
];

export const linksConfig = [
  {
    label: "Configuracion",
    to: "/configuracion",
    icon: <AiFillSetting />,
  },
  {
    label: "Salir",
    to: "/logout",
    icon: <FiLogOut />,
  },
];

export const linksModal = [
  {
    label: "Perfil",
    to: "/perfil",
    icon: <BiSolidUser />,
  },
  {
    label: "Mis compras",
    to: "/compras",
    icon: <AiFillShopping />,
  },
  {
    label: "Reportar un problema",
    to: "/reportError",
    icon: <BiCommentError />,
  },
];
