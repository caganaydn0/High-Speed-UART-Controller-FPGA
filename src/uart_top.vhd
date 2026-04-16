library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity uart_top is
    Port ( 
    
        clk        : in  STD_LOGIC;
        button        : in  STD_LOGIC; -- buton girişi
        tx_out     : out STD_LOGIC
        
    );
end uart_top;

architecture Behavioral of uart_top is
    -- Debounce sabitleri (100MHz için 20ms ≈ 2,000,000 cycle)
    constant DEBOUNCE_LIMIT : integer := 2000000;
    signal count_db : integer := 0;
    signal btn_debounced : std_logic := '0';
    signal btn_prev : std_logic := '0';
    signal tx_data : std_logic_vector(7 downto 0) := x"41"; -- A harfi
    
    -- UART sabitleri
    constant CLK_DIV : integer := 868; 
    type state_type is (IDLE, START, DATA, STOP);
    signal state : state_type := IDLE;
    signal count_uart : integer := 0;
    signal bit_idx : integer := 0;
    signal tx_reg : std_logic := '1';

begin

    tx_out <= tx_reg;

    -- 1. Debounce İşlemi
    process(clk)
    begin
        if rising_edge(clk) then
            btn_prev <= button;
            if button /= btn_prev then
                count_db <= 0;
            elsif count_db < DEBOUNCE_LIMIT then
                count_db <= count_db + 1;
            else
                btn_debounced <= button;
            end if;
        end if;
    end process;

    -- 2. UART State Machine (Button tetiklemeli)
    process(clk)
    begin
        if rising_edge(clk) then
            case state is
                when IDLE =>
                    tx_reg <= '1';
                    -- Sadece butona basıldığında (yükselen kenar) tetikle
                    if btn_debounced = '1' then
                        state <= START;
                        count_uart <= 0;
                    end if;
                    
                when START =>
                    tx_reg <= '0';
                    if count_uart < CLK_DIV - 1 then
                        count_uart <= count_uart + 1;
                    else
                        count_uart <= 0;
                        state <= DATA;
                        bit_idx <= 0;
                    end if;
                    
                when DATA =>
                    tx_reg <= tx_data(bit_idx); -- 'A' harfi
                    if count_uart < CLK_DIV - 1 then
                        count_uart <= count_uart + 1;
                    else
                        count_uart <= 0;
                        if bit_idx < 7 then
                            bit_idx <= bit_idx + 1;
                        else
                            state <= STOP;
                        end if;
                    end if;
                    
                when STOP =>
                    tx_reg <= '1';
                    if count_uart < CLK_DIV - 1 then
                        count_uart <= count_uart + 1;
                    else
                        state <= IDLE;
                    end if;
            end case;
        end if;
    end process;
end Behavioral;