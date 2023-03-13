import { Outlet } from 'react-router-dom';
import tw from 'twin.macro';

const ServerLayout = (): JSX.Element => {
  return (
    <div>
      <Outlet />
    </div>
  );
};

export default ServerLayout;
