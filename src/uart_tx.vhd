----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 02.03.2026 14:34:02
-- Design Name: 
-- Module Name: uart_tx - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity uart_tx is
    Port ( clk : in STD_LOGIC;
           tx_start : in STD_LOGIC;
           tx_tick : in STD_LOGIC;
           tx_data : in std_logic_vector(0 downto 3);
           tx_out : out STD_LOGIC;
           tx_done : out STD_LOGIC
           );
end uart_tx;

architecture Behavioral of uart_tx is

type state_type is ( IDLE, START_BIT, DATA_BIT, STOP_BIT);
signal state : state_type := IDLE;
signal bit_idx : integer range 0 to 7:= 0;
signal data_reg : std_logic_vector(0 downto 7):= (others => '0');

begin

process(clk)
begin

if (rising_edge(clk)) then

case state is
  when IDLE =>
    tx_out <= '1';
    tx_done <= '0';
    if tx_start = '1' then
      data_reg <= tx_data;
      state <= START_BIT;
    end if;
  
  when START_BIT =>
  if tx_tick = '1' then
        tx_out <= '0';
        state <= DATA_BIT;
        bit_idx <= 0;
  end if;
  
  when DATA_BIT =>
  if tx_tick = '1' then
        tx_out <= data_reg(bit_idx);
        if bit_idx = 7 then
          state <= STOP_BIT;
        else
          bit_idx <= bit_idx + 1;
  end if;
  end if;
  when STOP_BIT =>
  if tx_tick = '1' then
          tx_out <= '1'; 
          tx_done <= '1';
          state <= IDLE;
  end if;
end case;
end if;
end process;
end Behavioral;
